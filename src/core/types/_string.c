#include <obin.h>

#define __TypeName__ "__String__"

static OBehavior __BEHAVIOR__ = {0};

static obyte* __CHARS__[SCHAR_MAX] = {0};

#define _CHECK_SELF_TYPE(state, self, method) \
	if(!OAny_isString(self)) { \
		return obin_raise(state, oerrors(state)->TypeError, \
				__TypeName__"."#method "call from other type", self); \
	} \

static OAny _obin_string_empty(OState* state) {
	OAny result;

	result = obin_char_new(0);
	result.data.char_value.size = 0;
	return result;
}

typedef struct {
	OCELL_HEADER;
	ochar* data;
	omem_t capacity;
	omem_t size;
	oint hash;
} ObinString;

#define _string(any) ((ObinString*) OAny_toCell(any))

static ochar* _string_data(OAny any) {
	switch(any.type) {
	case EOBIN_TYPE_STRING:
		return  _string(any)->data;
		break;
	case EOBIN_TYPE_CHAR:
		opanic("CHAR TYPE ARE NOT MUTABLE");
		return NULL;
		break;
	default:
		return NULL;
	}
}
static ostring _string_const_data(OAny any) {
	switch(any.type) {
	case EOBIN_TYPE_STRING:
		return  _string(any)->data;
		break;
	case EOBIN_TYPE_CHAR:
		return (ostring)__CHARS__[any.data.char_value.char_data];
		break;
	default:
		return NULL;
	}
}

/* SIZE FOR BUFFER IN STACK USED TO WRITE INTS AND FLOATS TO STRING */

static oint _string_size(OAny any) {
	switch(any.type) {
	case EOBIN_TYPE_STRING:
		return _string(any)->size;
		break;
	case EOBIN_TYPE_CHAR:
		return any.data.char_value.size;
		break;
	default:
		return -1;
	}
}

#define _is_char(any) (any.type == EOBIN_TYPE_CHAR)
#define _is_string(any) (any.type == EOBIN_TYPE_STRING)
#define _is_empty(any) (_is_char(any) && any.data.char_value.size == 0)

/**********************************  TYPETRAIT ***********************************************/

static OAny __tostring__(OState* state, OAny self) {
	return obin_clone(state, self);
}

static OAny __tobool__(OState* state, OAny self) {
	return obin_bool_new(!_is_empty(self));
}

static OAny __length__(OState* state, OAny self) {
	_CHECK_SELF_TYPE(state, self, __length__);

	if(_is_char(self)){
		if(_is_empty(self)){
			return obin_integer_new(0);
		}
		return obin_integer_new(1);
	}

	return obin_integer_new(_string_size(self));
}

static OAny __hasitem__(OState* state, OAny self, OAny character) {
	OAny result;
	_CHECK_SELF_TYPE(state, self, __hasitem__);

	result = obin_string_index_of(state, self, character, ObinNil, ObinNil);

	return obin_equal(state, result, ointegers(state)->NotFound);
}

static OAny __getitem__(OState* state, OAny self, OAny key) {
	omem_t index;
	ochar result;
	_CHECK_SELF_TYPE(state, self, __item__);

	if(!OAny_isInt(key)){
		return obin_raise(state, oerrors(state)->TypeError,
				"String.__item__ key must be integer", key);
	}

	index = OAny_toInt(key);
	if(index < 0 || index >= _string_size(self)) {
		return obin_raise(state, oerrors(state)->TypeError,
				"String.__item__ invalid index", key);
	}

	result = _string_const_data(self)[index];
	return obin_char_new(result);
}

static OAny __compare__(OState* state, OAny self, OAny other) {
	omem_t result;
	_CHECK_SELF_TYPE(state, self, __compare__);

	if (!OAny_isString(other)) {
		return obin_raise(state, oerrors(state)->TypeError,
				"String.__compare__ argument is not string", other);
	}

	if (_string_size(self) < _string_size(other)) {
		return ointegers(state)->Lesser;
	}

	if (_string_size(self) > _string_size(other)) {
		return ointegers(state)->Greater;
	}

	result = ostrncmp(_string_const_data(self), _string_const_data(other),
			_string_size(self));

	if (result < 0) {
		return ointegers(state)->Lesser;
	}
	if (result > 0) {
		return ointegers(state)->Greater;
	}

	return ointegers(state)->Equal;
}

static OAny __hash__(OState* state, OAny self) {
	register oint hash = 0;
	register const ochar * cursor = 0;
	register oint length = 0;
	ObinHashSecret secret;

	_CHECK_SELF_TYPE(state, self, __hash__);

	if(_is_empty(self)){
		return obin_integer_new(0);
	}

	if(_is_char(self)) {
		return obin_integer_new((oint) _string_const_data(self)[0]);
	}

	/* return already hashed value */
	hash = _string(self)->hash;
	if(hash){
		return obin_integer_new(hash);
	}

	secret = obin_hash_secret();
	cursor = _string_const_data(self);
    hash = secret.prefix;
	hash ^= (*(cursor) << 7);
	length = _string_size(self);
	while(--length >= 0){
		hash = (1000003 * hash) ^ *cursor;
		cursor++;
	}

	hash ^= length;
	hash ^= secret.suffix;

	_string(self)->hash = hash;
	return obin_integer_new(hash);
}

static OAny __iterator__(OState* state, OAny self) {
	return obin_sequence_iterator_new(state, self);
}

static OAny __clone__(OState* state, OAny self) {
	return obin_string_from_carray(state, _string_const_data(self), _string_size(self));
}

static OAny _obin_string_blank(OState* state, omem_t length);

static OAny __add__(OState* state, OAny str1, OAny str2) {
	ochar* data;
	omem_t size;
	OAny result;

	_CHECK_SELF_TYPE(state, str1, __add__);

	if(!OAny_isString(str2)) {
		return obin_raise(state, oerrors(state)->TypeError,
						"String.__add__ invalid argument type, String expected ", str2);
	}

	if (_string_size(str1) == 0) {
		return obin_clone(state, str2);
	}
	if (_string_size(str2) == 0) {
		return obin_clone(state, str1);
	}

	size = _string_size(str1) + _string_size(str2);

	if (size == 0) {
		return ostrings(state)->Empty;
	}

	if (size == 1) {
		return obin_char_new(
				_string_size(str1) == 0 ?
						_string_const_data(str2)[0] : _string_const_data(str1)[0]);
	}

	result = _obin_string_blank(state, size);
	data = _string_data(result);
	omemcpy(data, _string_const_data(str1), _string_size(str1));
	omemcpy(data + _string_size(str1), _string_const_data(str2),
			_string_size(str2));

	return result;
}



/***********************************************************************************/
/* constructors */
OAny obin_string_new(OState* state, ostring data) {
	int len;

	len = ostrlen(data);
	if (len == 0) {
		return obin_string_from_carray(state, 0, 0);
	}

	return obin_string_from_carray(state, (ochar*) data, len);
}

OAny obin_char_new(ochar ch) {
	OAny result;

	result = OAny_new();
	result.type = EOBIN_TYPE_CHAR;
	result.data.char_value.char_data = ch;
	result.data.char_value.size = 1;
	return result;
}

static OAny _obin_string_from_carr(OState* state, ostring data, omem_t size) {
	omem_t capacity, body_size;
	ObinString* self;

	body_size = sizeof(ObinString);
	capacity = body_size + size + 1;
	self = (ObinString*) obin_allocate_cell(state, capacity);

	self->capacity = capacity;
	self->size = size;
	self->data = (ochar*) self + body_size;
	if(data != NULL) {
		omemcpy(self->data, data, self->size);
	}

	self->data[self->size] = '\0';

	return obin_cell_new(EOBIN_TYPE_STRING, (OCell*) self, &__BEHAVIOR__, ocells(state)->__String__);
}

static OAny _obin_string_blank(OState* state, omem_t length) {
	return _obin_string_from_carr(state, NULL, length);
}

/*@param data array without \0
 *@param size array size
 */
OAny obin_string_from_carray(OState* state, ostring data,
omem_t size) {
	/*empty string*/
	if (size == 0) {
		return _obin_string_empty(state);
	}
	if (size == 1) {
		return obin_char_new(data[0]);
	}

	return _obin_string_from_carr(state, data, size);
}


/* ******************** ATTRIBUTES ***********************************************/
ostring obin_string_cstr(OState* state, OAny self){
	return _string_const_data(self);
}

OAny obin_string_is_empty(OState* state, OAny self){
	if(!OAny_isString(self)) {
		return obin_raise(state, oerrors(state)->InternalError,
				"obin_string_is_empty call from other type", self);
	}
	return obin_tobool(state, __length__(state, self));
}
/******************************** MODIFICATIONS *************************************/
/*  function for modify char arrays , return 0 for stop iteration */
typedef int (*_string_modifier)(ochar* char_data, omem_t index);

/* clone string and modify it`s content by modifier */
OAny _clone_and_modify(OState* state, OAny self,
		_string_modifier modify) {
	OAny clone;
	omem_t i;
	if(_is_empty(self)) {
		return self;
	}
	if(_is_char(self)) {
		clone = self;
		/**Tricky part we send pointer to char value wit 0 index*/
		clone.data.char_value.char_data = modify((ochar*)&clone.data.char_value.char_data, 0);
		return clone;
	}

	clone = __clone__(state, self);

	for (i = 0; i < _string_size(clone); i++) {
		if (modify(_string_data(clone), i) == OFALSE) {
			break;
		}
	}

	return clone;
}

/*********************** CAPITALIZE *************************/
static int _capitalize_modify(ochar* data, omem_t index) {
	if (!isalpha(data[index])) {
		return OTRUE;
	}

	data[index] = toupper(data[index]);
	return OFALSE;
}

OAny obin_string_capitalize(OState* state, OAny self) {
	static _string_modifier modifier = &_capitalize_modify;
	_CHECK_SELF_TYPE(state, self, capitalize);

	return _clone_and_modify(state, self, modifier);
}

/*********************** CAPITALIZE WORDS*************************/
static int _capitalize_words_modify(ochar* data, omem_t index) {
	if ((index == 0 || isspace(data[index - 1])) && isalpha(data[index])) {
		data[index] = toupper(data[index]);
	}
	return OTRUE;
}

OAny obin_string_capitalize_words(OState* state, OAny self) {
	static _string_modifier modifier = _capitalize_words_modify;
	_CHECK_SELF_TYPE(state, self, capitalize_words);

	return _clone_and_modify(state, self, modifier);
}
/********************* UPPERCASE *************************/
static int _uppercase_modify(ochar* data, omem_t index) {
	data[index] = toupper(data[index]);
	return OTRUE;
}

OAny obin_string_to_uppercase(OState* state, OAny self) {
	static _string_modifier modifier = _uppercase_modify;
	_CHECK_SELF_TYPE(state, self, to_uppercase);

	return _clone_and_modify(state, self, modifier);
}

/********************* LOWERCASE ***************************/
static int _lowercase_modify(ochar* data, omem_t index) {
	data[index] = tolower(data[index]);
	return OTRUE;
}

OAny obin_string_to_lowercase(OState* state, OAny self) {
	static _string_modifier modifier = _lowercase_modify;
	_CHECK_SELF_TYPE(state, self, to_lowercase);

	return _clone_and_modify(state, self, modifier);
}

/************** CONDITIONS **************************************/
/*  function for checking string content by some condition*/
typedef int (*_string_condition)(ostring char_data, omem_t index);

/* check string content for condition */
OAny _check_condition(OState* state, OAny self,
		_string_condition condition) {
	omem_t i;

	for (i = 0; i < _string_size(self); i++) {
		if (condition(_string_const_data(self), i) == OFALSE) {
			return ObinFalse;
		}
	}

	return ObinTrue;
}
/*************************** IS_ALL_ALPHANUM **********************************/
static int _is_alphanum_condition(ostring data, omem_t index) {
	return isdigit(data[index]) || isalpha(data[index]);
}

OAny obin_string_is_alphanum(OState* state, OAny self) {
	_CHECK_SELF_TYPE(state, self, is_alphanum);

	return _check_condition(state, self, &_is_alphanum_condition);
}

/*************************** ISALPHA **********************************/
static int _is_alpha_condition(ostring data, omem_t index) {
	return isalpha(data[index]);
}

OAny obin_string_is_alpha(OState* state, OAny self) {
	_CHECK_SELF_TYPE(state, self, is_alpha);
	return _check_condition(state, self, &_is_alpha_condition);
}

/*************************** ISDIGIT **********************************/
static int _is_digit_condition(ostring data, omem_t index) {
	return isdigit(data[index]);
}

OAny obin_string_is_digit(OState* state, OAny self) {
	_CHECK_SELF_TYPE(state, self, is_digit);
	return _check_condition(state, self, &_is_digit_condition);
}
/*************************** IS LOWER **********************************/
static int _is_lower_condition(ostring data, omem_t index) {
	char ch = data[index];
	if(!isalpha(ch)) {
		/*skip other stuff*/
		return 1;
	}

	return islower(ch);
}

OAny obin_string_is_lower(OState* state, OAny self) {
	_CHECK_SELF_TYPE(state, self, is_lower);
	return _check_condition(state, self, &_is_lower_condition);
}
/*************************** IS UPPER **********************************/
static int _is_upper_condition(ostring data, omem_t index) {
	char ch = data[index];
	if(!isalpha(ch)) {
		/*skip other stuff*/
		return 1;
	}

	return isupper(ch);
}

OAny obin_string_is_upper(OState* state, OAny self) {
	_CHECK_SELF_TYPE(state, self, is_upper);
	return _check_condition(state, self, &_is_upper_condition);
}
/*************************** IS SPACE **********************************/
static int _is_space_condition(ostring data, omem_t index) {
	return isspace(data[index]);
}

OAny obin_string_is_space(OState* state, OAny self) {
	_CHECK_SELF_TYPE(state, self, is_space);
	return _check_condition(state, self, &_is_space_condition);
}
/************************* SEARCH ***************************************/
typedef OAny (*_string_finder)(OState* state, OAny haystack, OAny needle,
omem_t start, omem_t end);

OAny _obin_string_find(OState* state, OAny haystack, OAny needle,
		OAny start, OAny end, _string_finder finder) {
	omem_t pstart;
	omem_t pend;
	omem_t haystack_size;

	haystack_size = _string_size(haystack);
	if (OAny_isNil(start)) {
		pstart = 0;
	} else {
		if (OAny_toInt(start) < 0
				|| OAny_toInt(start) > haystack_size) {

			return obin_raise(state, oerrors(state)->RangeError,
					"String.search Invalid start index for search ", start);
		}

		pstart = (omem_t) OAny_toInt(start);
	}

	if (OAny_isNil(end)) {
		pend = haystack_size;
	} else {
		if (OAny_toInt(end) < 0 || OAny_toInt(end) > haystack_size
				|| OAny_toInt(end) < pstart) {

			return obin_raise(state, oerrors(state)->RangeError,
					"String.search Invalid end index for search ", end);
		}

		pend = (omem_t) OAny_toInt(end);
	}

	if ((pend - pstart) > _string_size(haystack)) {
		return obin_raise(state, oerrors(state)->RangeError,
					"String.search Invalid search range ",
					obin_tuple_pack(state, 2,
							obin_integer_new(pstart), obin_integer_new(pend)));
	}

	return finder(state, haystack, needle, pstart, pend);
}
/* ****************************** INDEXOF *************************************************************/
OAny _string_finder_left(OState* state, OAny haystack, OAny needle,
										omem_t start, omem_t end) {
	omem_t size_h;
	omem_t size_n;
	omem_t i;
	omem_t hi;
	omem_t ni;
	const ochar* data_h;
    const ochar* data_n;

    data_h = _string_const_data(haystack);
    data_n = _string_const_data(needle);
    size_h = _string_size(haystack);
    size_n = _string_size(needle);

	for (i = start; i < end; i++) {
		/*Is the needle at this point in the haystack?*/
		hi = i;
		ni = 0;
		while(ni < size_n && hi < size_h
				&& (data_h[hi]==data_n[ni]) ){
			ni++;
			hi++;
		}
		if (ni == size_n) {
			/* Found match! */
			return obin_integer_new(i);
		}
		/* Didn't match here.  Try again further along haystack. */
	}

	return ointegers(state)->NotFound;
}

OAny obin_string_index_of(OState* state, OAny self, OAny other,
		OAny start, OAny end) {
	_CHECK_SELF_TYPE(state, self, index_of);

	if(!OAny_isString(other)) {
		return obin_raise(state, oerrors(state)->TypeError,
				"String.indexof invalid argument type, string expected ", other);
	}

	return _obin_string_find(state, self, other, start, end,
			&_string_finder_left);
}

/* ****************************** LASTINDEXOF *************************************************************/
/*
 Return the highest index in the string
 where substring sub is found, such that sub is contained
 within s[start:end]. Optional arguments start and end
 are interpreted as in slice notation. Return STRING_INDEX_NOT_FOUND on failure.
 */
OAny _string_finder_right(OState* state, OAny haystack, OAny needle,
omem_t start, omem_t end) {
	omem_t i;
	omem_t hi;
	omem_t ni;
	const ochar* data_h;
    const ochar* data_n;

    data_h = _string_const_data(haystack);
    data_n = _string_const_data(needle);
	for (i = end - 1; i >= start; i--) {
		/*for is to creepy in that case, while is more readable */
		hi = i;
		ni = _string_size(needle) - 1;
		while (hi >= start && ni > 0 && (data_h[hi] == data_n[ni])) {
				--hi;
				--ni;
		}

		if (ni == 0) {
			/*Found match! */
			return obin_integer_new(i - _string_size(needle) + 1);
		}
		/* Didn't match here.  Try again further along haystack. */
	}

	return ointegers(state)->NotFound;
}

OAny obin_string_last_index_of(OState* state, OAny self, OAny other,
		OAny start, OAny end) {
	_CHECK_SELF_TYPE(state, self, last_index_of);

	if(!OAny_isString(other)) {
		return obin_raise(state, oerrors(state)->TypeError,
				"String.last_indexof invalid argument type, string expected ", other);
	}

	return _obin_string_find(state, self, other, start, end,
			&_string_finder_right);
}

/*********************** BUILDERS *******************************************/
/* TODO IMPLEMENT */
/*ObinAny obin_string_format(ObinState* state, ObinAny format, ...);*/

OAny obin_string_dublicate(OState* state, OAny self, OAny _count) {
	omem_t size;
	omem_t count;
	ochar* data;
	OAny result;

	_CHECK_SELF_TYPE(state, self, dublicate);

	if(_is_empty(self)) {
		return self;
	}

	if (OAny_isNil(_count)) {
		return obin_clone(state, self);
	}

	if(!OAny_isInt(_count)) {
		return obin_raise(state, oerrors(state)->TypeError,
				"String.dublicate invalid argument type, integer expected ", _count);
	}

	count = OAny_toInt(_count);

	size = _string_size(self) * count;
	result = _obin_string_blank(state, size);
	data = _string_data(result);
	for (; count > 0; count--, data += _string_size(self)) {
		omemcpy(data, _string_const_data(self), _string_size(self));
	}

	return result;
}

OAny obin_string_split(OState* state, OAny self, OAny separator) {
	OAny result;
	OAny curPos;
	omem_t current;
	omem_t previous;

	_CHECK_SELF_TYPE(state, self, split);

	if(!OAny_isString(separator)) {
		return obin_raise(state, oerrors(state)->TypeError,
						"String.split invalid argument type, String expected ", separator);
	}

	result = obin_array_new(state, ObinNil);

	if (_string_size(separator) > _string_size(self)) {
		/*can`t split */
		obin_array_push(state, result, obin_clone(state, self));
		return result;
	}

	current = 0;
	previous = 0;

	while (OTRUE) {
		curPos = _string_finder_left(state, self, separator, previous, _string_size(self));

		if (OAny_isTrue(obin_equal(state, curPos, ointegers(state)->NotFound))) {

			obin_array_push(state, result,
						obin_string_from_carray(state, _string_const_data(self) + previous,
								_string_size(self) - previous));
			return result;
		}
		current = OAny_toInt(curPos);
		if (current == 0) {
			previous = current + _string_size(separator);
			continue;
		}

		obin_array_push(state, result,
				obin_string_from_carray(state, _string_const_data(self) + previous,
						current - previous));

		previous = current + _string_size(separator);
	}

	return result;
}

OAny obin_string_join(OState* state, OAny self, OAny collection) {
	OAny iterator;
	OAny value;
	OAny result;
	oindex_t counter;

	_CHECK_SELF_TYPE(state, self, join);

	result = ostrings(state)->Empty;

	counter = OAny_toInt(obin_length(state, collection));
	if(counter==0) {
		return result;
	}

	iterator = obin_iterator(state, collection);

	while (OTRUE) {
		/*avoid appending self at end of string*/
		if(!(--counter)){
			break;
		}

		value = obin_next(state, iterator);
		result = __add__(state, result, value);
		result = __add__(state, result, self);
	}

	/*append last element*/
	value = obin_next(state, iterator);
	result = __add__(state, result, value);
	return result;
}

OAny obin_string_pack(OState* state, oindex_t count, ...){
	OAny array;
	oindex_t i;
	OAny item;
    va_list vargs;

	if(!OBIN_IS_FIT_TO_MEMSIZE(count)) {
		return obin_raise(state, oerrors(state)->TypeError,
						"String.pack invalid argument type, Invalid size", obin_integer_new(count));
	}

	array = obin_array_new(state, obin_integer_new(count));

    va_start(vargs, count);
    for (i = 0; i < count; i++) {
    	item = va_arg(vargs, OAny);
    	obin_array_push(state, array, item);
    }

    va_end(vargs);

    return obin_string_join(state, ostrings(state)->PrintSeparator, array);
}
/* //native
 str.startswith(prefix[, start[, end]])
 str.lstrip([chars])
 str.rstrip([chars])
 str.splitlines([keepends])
 */

OBehavior* obin_char_behavior() {
	return &__BEHAVIOR__;
}

static void _init_chars_cache() {
	int c = 0;

	for(c=0; c<=UCHAR_MAX; c++) {
		__CHARS__[c] = ocalloc(2, sizeof(ochar));
		__CHARS__[c][0] = c;
		__CHARS__[c][1] = 0;
	}
}
obool obin_module_string_init(OState* state) {
	_init_chars_cache();

	__BEHAVIOR__.__name__ = "__String__";
	__BEHAVIOR__.__tostring__ = __tostring__;
	__BEHAVIOR__.__tobool__ = __tobool__;
	__BEHAVIOR__.__clone__ = __clone__;
	__BEHAVIOR__.__compare__ = __compare__;
	__BEHAVIOR__.__hash__ = __hash__;

	__BEHAVIOR__.__iterator__ = __iterator__;
	__BEHAVIOR__.__length__ = __length__;
	__BEHAVIOR__.__getitem__ = __getitem__;
	__BEHAVIOR__.__hasitem__ = __hasitem__;
	__BEHAVIOR__.__add__ = __add__;

	obehaviors(state)->Char = &__BEHAVIOR__;

	/*strings proto*/
	ocells(state)->__String__ =  obin_cell_new(EOBIN_TYPE_CELL,
			obin_new(state, OCell), &__BEHAVIOR__, ocells(state)->__Cell__);


	ostrings(state)->Nil = obin_string_new(state, "Nil");
	ostrings(state)->True = obin_string_new(state, "True");
	ostrings(state)->False = obin_string_new(state, "False");
	ostrings(state)->Nothing = obin_string_new(state, "Nothing");
	ostrings(state)->PrintSeparator = obin_char_new(OBIN_PRINT_SEPARATOR);
	ostrings(state)->Empty = _obin_string_empty(state);
	ostrings(state)->Space = obin_char_new('\32');
	ostrings(state)->TabSpaces = obin_string_dublicate(state, ostrings(state)->Space, obin_integer_new(OBIN_COUNT_TAB_SPACES));

	return OTRUE;
}

#include <obin.h>
OBEHAVIOR_DECLARE(__BEHAVIOR__);

typedef struct {
	OCELL_HEADER;
	OAny path;
	ofile file;
	obool is_disposable;
} ObinFStream;

#define _fstream(any) ((ObinFStream*) OAny_toCell(any))
#define _fstream_file(any) (_fstream(any)->file)
#define _fstream_path(any) (_fstream(any)->path)
#define _fstream_is_disposable(any) (_fstream(any)->is_disposable)

OAny obin_fstream_from_file(OState* state, ofile file, obool is_disposable){

	ObinFStream* self;

	self = obin_new(state, ObinFStream);

	self->path = ostrings(state)->Empty;

	self->file = file;
	self->is_disposable = is_disposable;
	return obin_cell_new(EOBIN_TYPE_CELL, (OCell*)self, &__BEHAVIOR__, ocells(state)->__Cell__);
}

OAny obin_fstream_from_path(OState* state, OAny path, ostring mode){
	OAny result;
	ofile file = fopen(obin_string_cstr(state, path), mode);

	if(file == NULL) {
		obin_raise(state, oerrors(state)->IOError,
				"Unable to open file", path);
	}

	result = obin_fstream_from_file(state, file, OTRUE);
	_fstream_path(result) = path;
	return ObinNil;
}

OAny obin_fstream_write_va(OState* state, OAny self, ostring format, ...){
		int result;

	    va_list myargs;
	    va_start(myargs, format);
	    result = ovfprintf(_fstream_file(self), format, myargs);
	    va_end(myargs);

	    return obin_integer_new(result);
}

OAny obin_fstream_write(OState* state, OAny self, OAny any){
	return ObinNil;
}

OAny obin_fstream_close(OState* state, OAny self){
	if(!_fstream_is_disposable(self)) {
		obin_raise(state, oerrors(state)->IOError,
				"Resource is not disposable", ObinNil);
	}

	fclose(_fstream_file(self));
	_fstream_file(self) = NULL;

	return ObinNothing;
}

OAny obin_fstream_is_open(OState* state, OAny self) {
	if(_fstream_file(self) == NULL) {
		return ObinFalse;
	}

	return ObinTrue;
}

static OAny __tostring__(OState* state, OAny self) {
	return obin_string_new(state, "<File: "OBIN_POINTER_FORMATTER" >");
}

static void __destroy__(OState* state, OCell* cell) {
	ObinFStream* self = (ObinFStream*) cell;

	if(self->file && self->is_disposable) {
		obin_fstream_close(state,
				obin_cell_to_any(EOBIN_TYPE_CELL, (OCell*)self));
	}
}

OBEHAVIOR_DEFINE(__BEHAVIOR__,
		"__FStream__",
		OBEHAVIOR_MEMORY(__destroy__, 0),
		OBEHAVIOR_BASE(__tostring__, 0, 0, 0, 0),
		OBEHAVIOR_COLLECTION_NULL,
		OBEHAVIOR_GENERATOR_NULL,
		OBEHAVIOR_NUMBER_CAST_NULL,
		OBEHAVIOR_NUMBER_OPERATIONS_NULL
);


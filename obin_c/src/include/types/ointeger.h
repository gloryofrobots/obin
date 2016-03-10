#ifndef OINTEGER_H_
#define OINTEGER_H_

#include "obuiltin.h"

obool ointeger_init(OState* S);


OAny OInteger(oint number);
OAny OInteger_toFloat(OAny integer);
OAny OInteger_toChar(OAny integer);

#define OInteger_isFitToMemsize(number) \
	(obin_any_integer(number) > 0 && obin_any_integer(number) < OBIN_MEM_MAX)

#endif /* OINTEGER_H_ */
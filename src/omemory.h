#ifndef OBIN_OMEMORY_H_
#define OBIN_OMEMORY_H_
#include "otypes.h"



typedef struct{
	obin_integer mark;
} ObinCellGCInfo;

/*IT EMPTY FOR NOW */
#define OBIN_CELL_HEADER \
	ObinCellGCInfo gc_info

#define OBIN_DEFINE_TYPE_TRAIT(type) type type_trait

struct _ObinCell {
	OBIN_CELL_HEADER;
	OBIN_DEFINE_TYPE_TRAIT(ObinCellTrait);
};


/*
 * Stolen from Python.
 * here we have safe guards for malloc(0) that can have unexpected behavior on many platforms
*/

#define ObinMem_MALLOC(n) ((obin_mem_t)(n) > OBIN_MEM_MAX? NULL \
				: malloc((n) ? (n) : 1))

#define ObinMem_REALLOC(p, n)	((obin_mem_t)(n) > (obin_mem_t)OBIN_MEM_MAX  ? NULL \
				: realloc((p), (n) ? (n) : 1))

#define ObinMem_FREE	free

#define obin_memcpy memcpy

#ifndef OBIN_MEMORY_DEBUG

obin_pointer obin_malloc(obin_mem_t size);

obin_pointer obin_malloc_and_fill(obin_mem_t size);

obin_pointer obin_realloc(obin_pointer ptr, obin_mem_t size) ;

obin_pointer obin_memdup(obin_pointer ptr, obin_mem_t elements, obin_mem_t element_size );

#else
/* Redirect all memory operations debugging allocator. */
#endif


#define obin_malloc_type(type) \
	 ( (type *) obin_malloc(sizeof(type)) )

#define obin_malloc_collection(type, n) \
  ( ((obin_mem_t)(n) > OBIN_MEM_MAX / sizeof(type)) ? NULL :	\
	( (type *) obin_malloc((n) * sizeof(type)) ) )

#define obin_realloc_type(p, type, n) \
  ( (p) = ((obin_mem_t)(n) > OBIN_MEM_MAX / sizeof(type)) ? NULL :	\
	(type *) obin_realloc((p), (n) * sizeof(type)) )


#endif
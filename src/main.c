#include <stdlib.h>
#include <stdio.h>
#include "otypes.h"

/* An animal --------------------------------------------------------------*/
typedef struct ANIMAL_DATA {
    int weight;
    const char * name;
} ANIMAL_DATA;

typedef struct ANIMAL {
    union {
        ANIMAL_DATA animal;
    } base;
} ANIMAL;

/* This macro perfoms like a typesafe cast */
#define GETANIMAL(self) (&(self)->base.animal)

/* Accessor macros (syntactic-sugar) */
#define weight(self)    (GETANIMAL(self)->weight)
#define name(self)      (GETANIMAL(self)->name)

/* An insect is an animal -------------------------------------------------*/
typedef struct INSECT_DATA {
    union {
        ANIMAL_DATA animal;
    } base;
    int exoskeleton;
} INSECT_DATA;

typedef struct INSECT {
    union {
        INSECT_DATA insect;
        ANIMAL_DATA animal;
    } base;
} INSECT;

#define GETINSECT(self)   (&(self)->base.insect)
#define exoskeleton(self) (GETINSECT(self)->exoskeleton)

/* An mammal is also an animal --------------------------------------------*/
typedef struct MAMMAL_DATA {
    union {
        ANIMAL_DATA animal;
    } base;
    int fur;
} MAMMAL_DATA;

typedef struct MAMMAL {
    union {
        MAMMAL_DATA mammal;
        ANIMAL_DATA animal;
    } base;
} MAMMAL;

#define GETMAMMAL(self) (&(self)->base.mammal)
#define fur(self)       (GETMAMMAL(self)->fur)

/* An monkey is a mammal with a tail --------------------------------------*/
typedef struct MONKEY_DATA {
    union {
        MAMMAL mammal;
        ANIMAL animal;
    } base;

    int tail;
} MONKEY_DATA;

typedef struct MONKEY {
    union {
        MONKEY_DATA monkey;
        MAMMAL_DATA mammal;
        ANIMAL_DATA animal;
    } base;
} MONKEY;

#define GETMONKEY(self) (&(self)->base.monkey)
#define tail(self)      (GETMONKEY(self)->tail)

/* An human is a mammal with a opposable thumb ----------------------------*/
typedef struct HUMAN_DATA {
    union {
        MAMMAL mammal;
        ANIMAL animal;
    } base;
    int thumb;
} HUMAN_DATA;

typedef struct HUMAN {
    union {
        HUMAN_DATA human;
        /* MAMMAL_DATA mammal; Conversion to MAMMAL_DATA is hidden
                               So this is a private base class */
        ANIMAL_DATA animal;
    } base;
} HUMAN;

#define GETHUMAN(self) (&(self)->base.human)
#define thumb(self)    (GETHUMAN(self)->thumb)

void print_animal(ANIMAL* animal) {
    printf("\n\n");
    printf("%s animal has weight %i\n\n", name(animal), weight(animal));
}

void print_human(HUMAN* human) {
    /* Humans have weight and thumbs */
    printf("%s the human has weight %i\n", name(human), weight(human));
    printf("%s the human has thumb %i\n\n", name(human), thumb(human));
}
/* Trying out inheritance in C ------------------------------------------- */


int main2(void)
{
    ANIMAL unknown;
    INSECT beetle;
    MAMMAL beaver;
    MONKEY george;
    HUMAN programmer;
    
    /* A generic animal */
    weight(&unknown) = 1;
    name(&unknown) = "unknown";

    /* A beetle with a thick exoskeleton */
    weight(&beetle) = 1;
    name(&beetle) = "Herbie";
    exoskeleton(&beetle) = 100;

    /* A furry beaver */
    weight(&beaver) = 10;
    name(&beaver) = "Barry";
    fur(&beaver) = 5;
    
    /* The monkey has a long tail */
    weight(&george) = 10;
    name(&george) = "George";
    fur(&george) = 1;
    tail(&george) = 10;

    /* Programmers are humans */
    weight(&programmer) = 150;
    name(&programmer) = "Steve";
/*    fur(&programmer) = 1;   ERROR: No public access to MAMMAL base class */
    thumb(&programmer) = 2;
  
    print_animal((ANIMAL*)&programmer);
    print_human(&programmer);

    return 0;
    /* Animals have weight */
    printf("\n\n");
    printf("%s animal has weight %i\n\n", name(&unknown), weight(&unknown));

    /* Beetles have weight and exoskeleton */
    printf("%s the beetle has weight %i\n", name(&beetle), weight(&beetle));
    printf("%s the beetle has exoskeleton %i\n\n", name(&beetle), exoskeleton(&beetle));

    /* Mammals have weight and fur */
    printf("%s the beaver has weight %i\n", name(&beaver), weight(&beaver));
    printf("%s the beaver has fur %i\n\n", name(&beaver), fur(&beaver));

    /* Monkeys have weight, fur and tails */
    printf("%s the monkey has weight %i\n", name(&george), weight(&george));
    printf("%s the monkey has fur %i\n", name(&george), fur(&george));
    printf("%s the monkey has tail %i\n\n", name(&george), tail(&george));

    /* Humans have weight and thumbs */
    printf("%s the programmer has weight %i\n", name(&programmer), weight(&programmer));
    printf("%s the programmer has thumb %i\n\n", name(&programmer), thumb(&programmer));

    /* Accessing a hidden base class gets a compile time error */
    /*fur(&programmer);          ERROR */

    /* The wrong function gets a compile-time error */
    /*tail(&programmer);         ERROR */
    /*exoskeleton(&programmer);  ERROR */
    /*exoskeleton(&george);      ERROR */

    return 0;
}

// buffer must have length >= sizeof(int) + 1
// Write to the buffer backwards so that the binary representation
// is in the correct order i.e.  the LSB is on the far right
// instead of the far left of the printed string
char *int2bin(int a, char *buffer, int buf_size) {
	int i = 0;
    buffer += (buf_size - 1);

    for (i = 31; i >= 0; i--) {
        *buffer-- = (a & 1) + '0';

        a >>= 1;
    }

    return buffer;
}
enum {
    ST_SMI_TAG,
    ST_POINTER_TAG,
    ST_CHARACTER_TAG,
    ST_MARK_TAG,
};

uintptr_t
st_tag_pointer (void* p)
{
    return ((uintptr_t) p) + ST_POINTER_TAG;
}

uintptr_t *
st_detag_pointer (uintptr_t oop)
{
    return (uintptr_t *) (oop - ST_POINTER_TAG);
}

#define BUF_SIZE 33
int main() {
    char buffer[BUF_SIZE];
    buffer[BUF_SIZE - 1] = '\0';

    int2bin(0xFF000000, buffer, BUF_SIZE - 1);

    printf("a = %s\n", buffer);
    printf("l = %ld \n", LONG_MAX);
    printf("i = %ld \n", INT_MAX);
    printf("s = %ld \n", SSIZE_MAX);
    printf("u = %f \n",(float) UINTPTR_MAX);

    printf("l = %ld \n", sizeof(long));
    printf("i = %ld \n", sizeof(int));
    printf("s = %ld \n", sizeof(size_t));
    printf("u = %0.f \n",(float) sizeof(uintptr_t));
    uintptr_t max = st_tag_pointer((void*) UINTPTR_MAX);
    printf("t = %0.f \n",(float) max);
    uintptr_t restore = st_detag_pointer(max);
    printf("r = %0.f \n",(float) restore);
}

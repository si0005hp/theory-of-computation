/* Nonnegative integers */
const ZERO = (p) => (x) => x;
const ONE = (p) => (x) => p(x);
const TWO = (p) => (x) => p(p(x));
const THREE = (p) => (x) => p(p(p(x)));
const FIVE = (p) => (x) => p(p(p(p(p(x)))));
const FIFTEEN = (p) => (x) => p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(x)))))))))))))));
// prettier-ignore
const HUNDRED = (p) => (x) => p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(x))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))));

/* Booleans */
const TRUE = (x) => (y) => x;
const FALSE = (x) => (y) => y;
const IF = (b) => b;

/* Pairs */
const PAIR = (a) => (b) => (f) => f(a)(b);
const LEFT = (f) => f((x) => (y) => x);
const RIGHT = (f) => f((x) => (y) => y);

/* Arithmetic */
const INCREMENT = (n) => (p) => (x) => p(n(p)(x));
const SLIDE = (p) => PAIR(RIGHT(p))(INCREMENT(RIGHT(p)));
const DECREMENT = (n) => LEFT(n(SLIDE)(PAIR(ZERO)(ZERO)));
const ADD = (m) => (n) => n(INCREMENT)(m);
const SUBTRACT = (m) => (n) => n(DECREMENT)(m);
const MULTIPLY = (m) => (n) => n(ADD(m))(ZERO);
const POWER = (m) => (n) => n(MULTIPLY(m))(ONE);

const IS_ZERO = (n) => n((x) => FALSE)(TRUE);
const IS_LESS_OR_EQUAL = (m) => (n) => IS_ZERO(SUBTRACT(m)(n));

/* Combinators */
const Y = (f) => ((x) => f(x(x)))((x) => f(x(x)));
const Z = (f) => ((x) => f((y) => x(x)(y)))((x) => f((y) => x(x)(y)));

const MOD = Z((f) => (m) => (n) =>
  IF(IS_LESS_OR_EQUAL(n)(m))(/*then*/ (x) => f(SUBTRACT(m)(n))(n)(x))(
    /*else*/ m
  )
);

const DIV = Z((f) => (m) => (n) =>
  IF(IS_LESS_OR_EQUAL(n)(m))(
    /*then*/ (x) => INCREMENT(f(SUBTRACT(m)(n))(n))(x)
  )(/*else*/ ZERO)
);

/* Lists */
const EMPTY = PAIR(TRUE)(TRUE);
const UNSHIFT = (l) => (x) => PAIR(FALSE)(PAIR(x)(l));
const IS_EMPTY = LEFT;
const FIRST = (l) => LEFT(RIGHT(l));
const REST = (l) => RIGHT(RIGHT(l));

const RANGE = Z((f) => (m) => (n) =>
  IF(IS_LESS_OR_EQUAL(m)(n))(/*then*/ (x) => UNSHIFT(f(INCREMENT(m))(n))(m)(x))(
    /*else*/ EMPTY
  )
);

const FOLD = Z((f) => (l) => (x) => (g) =>
  IF(IS_EMPTY(l))(/*then*/ x)(/*else*/ (y) => g(f(REST(l))(x)(g))(FIRST(l))(y))
);

const MAP = (k) => (f) => FOLD(k)(EMPTY)((l) => (x) => UNSHIFT(l)(f(x)));

const PUSH = (l) => (x) => FOLD(l)(UNSHIFT(EMPTY)(x))(UNSHIFT);

/* Strings */
const TEN = MULTIPLY(TWO)(FIVE);
const B = TEN;
const F = INCREMENT(B);
const I = INCREMENT(F);
const U = INCREMENT(I);
const ZED = INCREMENT(U);

const FIZZ = UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(EMPTY)(ZED))(ZED))(I))(F);
const BUZZ = UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(EMPTY)(ZED))(ZED))(U))(B);
const FIZZBUZZ = UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(BUZZ)(ZED))(ZED))(I))(F);

const TO_DIGITS = Z((f) => (n) =>
  PUSH(
    IF(IS_LESS_OR_EQUAL(n)(DECREMENT(TEN)))(/*then*/ EMPTY)(
      /*else*/ (x) => f(DIV(n)(TEN))(x)
    )
  )(MOD(n)(TEN))
);

const SOLUTION = MAP(RANGE(ONE)(HUNDRED))((n) =>
  IF(IS_ZERO(MOD(n)(FIFTEEN)))(
    /*then*/
    FIZZBUZZ
  )(
    /*else*/
    IF(IS_ZERO(MOD(n)(THREE)))(
      /*then*/
      FIZZ
    )(
      /*else*/
      IF(IS_ZERO(MOD(n)(FIVE)))(
        /*then*/
        BUZZ
      )(
        /*else*/
        TO_DIGITS(n)
      )
    )
  )
);

/* Helpers */
function to_integer(proc) {
  return proc((n) => n + 1)(0);
}

function to_boolean(proc) {
  return proc(true)(false);
}

function to_array(proc) {
  const array = [];
  while (!to_boolean(IS_EMPTY(proc))) {
    array.push(FIRST(proc));
    proc = REST(proc);
  }
  return array;
}

function to_char(c) {
  return "0123456789BFiuz".charAt(to_integer(c));
}

function to_string(s) {
  return to_array(s)
    .map((c) => to_char(c))
    .join("");
}

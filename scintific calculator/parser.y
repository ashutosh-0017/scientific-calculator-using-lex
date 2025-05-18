%{
#include <stdio.h>
#include <math.h>
#include <string.h>
#include "lex.yy.c"

void yyerror(char *s);
extern int yylex();

%}

%union {
    float fval;
    char *str;
}

%token <fval> NUMBER
%token <str> FUNC
%token PLUS MINUS MULT DIV POW
%token LPAREN RPAREN
%token EOL

%type <fval> expr

%left PLUS MINUS
%left MULT DIV
%left NEG
%right POW

%%

input:     
        | input line
        ;

line:       EOL
        | expr EOL { printf("Result: %g\n", $1); }
        ;

expr:       NUMBER              { $$ = $1; }
        | expr PLUS expr        { $$ = $1 + $3; }
        | expr MINUS expr       { $$ = $1 - $3; }
        | expr MULT expr        { $$ = $1 * $3; }
        | expr DIV expr         { $$ = $1 / $3; }
        | MINUS expr %prec NEG  { $$ = -$2; }
        | expr POW expr         { $$ = pow($1, $3); }
        | FUNC LPAREN expr RPAREN {
              if (strcmp($1, "sin") == 0) $$ = sin($3 * M_PI / 180.0); // Degrees to radians
              else if (strcmp($1, "cos") == 0) $$ = cos($3 * M_PI / 180.0);
              else if (strcmp($1, "tan") == 0) $$ = tan($3 * M_PI / 180.0);
              else if (strcmp($1, "log") == 0) $$ = log10($3);
              else if (strcmp($1, "ln") == 0) $$ = log($3);
              else if (strcmp($1, "sqrt") == 0) $$ = sqrt($3);
              else if (strcmp($1, "exp") == 0) $$ = exp($3);
              free($1);
          }
        | LPAREN expr RPAREN    { $$ = $2; }
        ;

%%

void yyerror(char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    yyparse();
    return 0;
}
%{
#include "y.tab.h"
#include <math.h>
#include <string.h>
%}

%%

[ \t]       ; 
[0-9]+(\.[0-9]+)? { yylval.fval = atof(yytext); return NUMBER; }
sin|cos|tan|log|ln|sqrt|exp { yylval.str = strdup(yytext); return FUNC; }
pi          { yylval.fval = M_PI; return NUMBER; }
e           { yylval.fval = M_E; return NUMBER; }
"+"         { return PLUS; }
"-"         { return MINUS; }
"*"         { return MULT; }
"/"         { return DIV; }
"^"         { return POW; }
"("         { return LPAREN; }
")"         { return RPAREN; }
"\n"        { return EOL; }
.           { printf("Unknown character: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}
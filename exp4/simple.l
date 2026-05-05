%{
#include "y.tab.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int lexical_error = 0;
%}

%%
int|float|if|else|while|return {
    printf("KEYWORD %s\n", yytext);
    return KEYWORD;
}

[a-zA-Z_][a-zA-Z0-9_]* {
    printf("IDENTIFIER %s\n", yytext);
    yylval.sval = strdup(yytext);
    return IDENTIFIER;
}

[0-9]+ {
    printf("INTEGER %s\n", yytext);
    yylval.ival = atoi(yytext);
    return INTEGER;
}

"+"|"-"|"*"|"/"|"="|"<"|">" {
    printf("OP %s\n", yytext);
    return yytext[0];
}

";"|"("|")"|"{"|"}" {
    printf("DELIM %s\n", yytext);
    return yytext[0];
}

[ \t\n]+ ;

. {
    printf("LEXICAL ERROR : %s\n", yytext);
    lexical_error = 1;
}

%%

int yywrap() {
    return 1;
}


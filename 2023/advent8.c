#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {false, true} bool;
#define MAXLEN 1000
#define LOG (1ULL<<33) - 1

char nodes[MAXLEN][4];
int graph [MAXLEN][2];
bool isz [MAXLEN];
bool isa [MAXLEN];
int nr_nodes;

char line[MAXLEN];

int find(char *s) {
    for (int i=0; i<nr_nodes; i++) {
        if (strcmp(nodes[i], s) == 0) {
            return i;
        }
    }
    strcpy(nodes[nr_nodes], s);
    isz[nr_nodes] = (s[2] == 'Z');
    isa[nr_nodes] = (s[2] == 'A');
    return nr_nodes++;
}

int main(int argc, char **argv) {
    char n1[4], n2[4], n3[4];
    scanf("%s", line);
    scanf("");
    while (scanf("%3s = (%3s, %3s)", n1, n2, n3) > 0) {
        int i1 = find(n1), i2 = find(n2), i3 = find(n3);
        // printf("%d %d %d\n", i1, i2, i3);
        graph[i1][0] = i2;
        graph[i1][1] = i3;
    }

    int current[1000];
    int current_len = 0;

    for (int i=0; i<nr_nodes; i++) {
        if (isa[i]) current[current_len++] = i;
    }

    unsigned long long steps = 0;
    int line_pointer = 0;
    int line_len = strlen(line);

    bool all_z = false;
    for (;!all_z;steps++, line_pointer=(line_pointer+1)%line_len) {
        int lr = (line[line_pointer] == 'L') ? 0 : 1;
        all_z = true;
        for (int i=0; i<current_len; i++) {
            // printf("%d ", current[i]);
            all_z = all_z && isz[current[i]];
            current[i] = graph[current[i]][lr];
        }
        if ((steps & LOG) == LOG) {
            fprintf(stderr, ".");
            // printf("\nsteps %llu %llu\n", steps, steps & LOG);
        }
        // printf("(%llu) \n", steps);
    }
    printf("\nsteps %llu\n", --steps);
}

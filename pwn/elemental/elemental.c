#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

#define LEN 2000

char *elements[] = {
    "H",  "He", "Li", "Be", "B",  "C",  "N",  "O",  "F",  "Ne", "Na", "Mg",
    "Al", "Si", "P",  "S",  "Cl", "Ar", "K",  "Ca", "Sc", "Ti", "V",  "Cr",
    "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y",  "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
    "In", "Sn", "Sb", "Te", "I",  "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf ",
    "Ta", "W",  "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po",
    "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U",  "Np", "Pu", "Am", "Cm",
    "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs",
    "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"};

typedef struct hash_set {
  char **data;
  size_t len;
} set_t;

size_t hash(char *s, size_t peak) {
  if (s[1] == 0x00) {
    return s[0] % peak;
  } else {
    return (s[0] + s[1] * s[1]) % peak;
  }
  return 0;
}

// Open addressing + quadratic probing
void set_add(set_t *set, char *s) {
  size_t key = hash(s, set->len);
  while (set->data[key] != NULL) {
    key = (key * key) % set->len;
  }
  set->data[key] = s;
}

set_t *init_set(size_t size) {
  size_t len = size * 3;
  set_t *set = malloc(sizeof(set_t));
  set->len = len;
  set->data = calloc(len, sizeof(char *));

  for (size_t i = 0; i < sizeof(elements) / sizeof(char *); i++) {
    set_add(set, elements[i]);
  }

  return set;
}

bool set_find(set_t *set, char *s) {
  size_t key = hash(s, set->len);
  while (set->data[key] != NULL) {
    if (!strcmp(set->data[key], s)) {
      return true;
    }
    key = (key * key) % set->len;
  }
  return false;
}

bool is_upper(char c) { return c >= 65 && c < 65 + 26; }
bool is_lower(char c) { return c >= 97 && c < 97 + 26; }

bool check_buf(set_t *set, char *buf, size_t len) {
  char element[3];
  element[2] = 0x00;
  for (size_t i = 0; i < len - 1; i++) {
    if (is_upper(buf[i])) {
      element[0] = buf[i];
      if (i == len || !is_lower(buf[i + 1])) {
        element[1] = 0x00;
      } else {
        element[1] = buf[i + 1];
        i++;
      }
    }

    if (!set_find(set, element)) {
      return false;
    }
  }

  return true;
}

int main(int arg, char *argv[]) {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  set_t *set = init_set(LEN);

  char *buf = (char *)mmap(0, LEN, PROT_READ | PROT_WRITE | PROT_EXEC,
                           MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  memset(buf, 0, LEN - 1);

  printf("Sad reacts only\n>>> ");
  fgets(buf, LEN - 2, stdin);

  if (check_buf(set, buf, strlen(buf))) {
    printf("Cooking it up...\n");
    ((void (*)())buf)();
  } else {
    printf("Sorry, go back to school\n");
  }
  return 0;
}

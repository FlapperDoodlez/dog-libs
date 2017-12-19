# dog-libs
---

## What is it
dog-libs is a game where players have to fill in the blanks of phrases and short stories—without knowing what the phrase or short story actually is—resulting in wacky outcomes.

This application was originally created to be used as a sample application as part of a longform guide on monitoring GKE using Datadog. The guide can be found [here](https://datadoghq.com/blog/monitor-google-kubernetes-engine/).

## How do I use it?

dog-libs is intended to be deployed on a GKE cluster. Follow the steps listed in [this guide](https://datadoghq.com/blog/monitor-google-kubernetes-engine/) to deploy it :)

### Create an adlib

To create an adlib,

1. visit the index page and click on "create your own lib".
2. give your adlib a name (make sure it doesn't reveal too much of the story).

>Old Macdonald
3. list the different entries you want players to submit (separate each entry with a comma).

>adjective, noun, animal, noise`
4. write your lib such that each intended entry is replaced with a `{n}` where `n` is a number corresponding to the entry (`n` is zero-indexed)

>{0} Macdonald had a {1}, E-I-E-I-O. And on that {1} he had an {2}, E-I-E-I-O. With a {3} {3} here and a {3} {3} there, here a {3}, there a {3}, everywhere a {3} {3}, {0} Macdonald had a {1}, E-I-E-I-O.
`
### Enter a solution

To enter a solution,

1. visit the index page to randomly retrieve a submitted adlib
2. fill in the entries with the appropriate words (or phrases)
3. click "submit" and read the adlib with the blanks filled in with your solution

### View the popular solution

dog-libs keeps track of what the most popular words are for each entry. To view the popular solution for an adlib,

1. visit the index page to randomly retrieve a submitted adlib
2. click "view popular" solution
3. read the adlib with the blanks filled in with the most popular words for that adlib

build:
    pdm run make-up

publish: build
    cd out && git add . && git commit -a -m "A-Set, You Bet!" && git push

next:
    pdm run next-ep romance

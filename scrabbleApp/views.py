from django.http import HttpResponse
import codecs


def get_words(n=99):
    return filter(lambda x: len(x) <= n,
                  codecs.open('slowa-win.txt', encoding='windows-1250').read().split('\r\n')[:-1])


MAX = 15
lines = get_words(MAX)
tree = {'depth': 0, 'words': []}


def add_to_map(word):
    ref = tree
    depth = 0
    for letter in sorted(word):
        depth += 1
        if letter not in ref:
            ref[letter] = {'depth': depth, 'words': []}
        ref = ref[letter]
    ref['words'] += [word]


for w in lines:
    add_to_map(w)


def collect(_tree, word, blank, missed, min_length=0):
    ret = []

    if missed > MAX - min_length:
        return ret

    keys = _tree.keys()

    if _tree['depth'] > min_length:
        ret += _tree['words']
    keys.remove('words')
    keys.remove('depth')

    for letter in keys:
        child = _tree[letter]
        if len(word) > 0 and letter == word[0]:
            ret += collect(child, word[1:], blank, missed, min_length)
        elif letter in word:
            ret += collect(child, word[word.index(letter) + 1:], blank, missed + word.index(letter) + 1, min_length)
        elif blank > 0:
            if blank > 3:
                print blank
            ret += collect(child, word, blank - 1, missed, min_length)

    return ret


def test(request):
    query = sorted(request.GET.get('q', ''))
    all_words = request.GET.get('all', False)
    length = len(query)
    blank = query.count('?')
    query = query[blank:]
    min_length = 2 if all_words else max(length - 2, 2)
    result = {i: [] for i in range(min_length, length + 1)}
    if length > 0:
        words = collect(tree, query, blank, -99 if all_words else 0, min_length)
        for word in words:
            result[len(word)] += [word]

        resp_text = ""
        for key in sorted(result.keys(), reverse=True):
            resp_text += str(key) + ":<br/>"
            for word in sorted(result[key]):
                resp_text += word + "<br/>"

        return HttpResponse(resp_text)
    else:
        return HttpResponse("""
        <form>
            <input name='q' type='text'/>
            <input name='all' type='checkbox'/>
            <button type='submit'> go </button>
        </form>
""")

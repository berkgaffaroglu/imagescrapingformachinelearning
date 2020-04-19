i = -1
with open('tags.txt', 'r') as file:
    tags = file.read()
    tagList = list()
    for tag in tags.split(','):
        tagList.append(tag)
def tagChooser():
    global i

    i += 1
    try:
      return tagList[i]
    except Exception:
      return -1

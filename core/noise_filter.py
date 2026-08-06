# filtru zgomot - ce ignora - 0 credite
ZGOMOT = ["Generate Video", "Generate Speech", "preview", "email"]
def este_zgomot(a):
    return any(z.lower() in a.lower() for z in ZGOMOT)
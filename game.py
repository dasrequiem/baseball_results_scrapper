class game:
    titulo = ''
    link = ''
    download_link = ''
    downloaded = False

    def __init__(self, titulo, link, download_link='', downloaded=False):
        self.titulo = titulo
        self.link = link
        self.download_link = ''

    def getValuesCSV(self):
        return '{},{},{},{}'.format(self.titulo, self.link, self.download_link, str(self.downloaded))

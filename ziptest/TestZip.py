import zipfile
import os


def appendToZipFile(sourcesPath, ):
    pass

if __name__ == '__main__':
    rootzip = zipfile.ZipFile('H:\\eclipse_workspace\\ZmnWap\\root.zip', 'w', zipfile.ZIP_DEFLATED)
    cssPath = 'H:\\eclipse_workspace\\ZmnWap\\WebRoot\\js'
    cssPathLen = cssPath.rindex('\\')
    for dirpath, dirnames, filenames in os.walk(cssPath):
        for filename in filenames:
            pathfile = os.path.join(dirpath, filename)
            srcname = pathfile[cssPathLen:].strip(os.path.sep)
            rootzip.write(pathfile, srcname)
    rootzip.close()
    pass
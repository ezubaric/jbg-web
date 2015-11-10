# Extrace media coverage from LaTeX source
import sys

kSTART = "\\headedsection{{\\bf Media Coverage}}{}{"
kSTOP = "\\end{enumerate}"

if __name__ == "__main__":
    media = open(sys.argv[1]).read().split(kSTART)[1]
    media = media.split(kSTOP)[0]

    o = open(sys.argv[2], 'w')
    o.write(media)
    o.write(kSTOP)

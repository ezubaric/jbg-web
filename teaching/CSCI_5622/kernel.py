import numpy as np

def read_data(filename):
    data = open(filename, 'r').readlines()

    y = np.array(list(int(x.split()[0]) for x in data))
    x = np.array(list((float(x.split()[1].split(":")[1]),
                       float(x.split()[2].split(":")[1])) for x in data))

    return x, y

def plot_model(X, Y, clf, fignum=0):
    # plot the line, the points, and the nearest vectors to the plane
    plt.figure(fignum, figsize=(4, 3))
    plt.clf()

    plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80,
                facecolors='none', zorder=10)
    plt.scatter(X[:, 0], X[:, 1], c=Y, zorder=10, cmap=plt.cm.Paired)

    plt.axis('tight')
    x_min = min(X[:, 0])
    x_max = max(X[:, 0])
    y_min = min(X[:, 1])
    y_max = max(X[:, 1])

    XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
    Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(XX.shape)
    plt.figure(fignum, figsize=(4, 3))
    plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
    plt.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'],
                levels=[-.5, 0, .5])

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.xticks(())
    plt.yticks(())

    plt.show()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from sklearn import svm

    fignum = 0
    X, Y = read_data("ex8a.txt")
    for kk, dd, gg, cc in [('linear', 0, 0, 0),
                           ('poly', 1, 0, 5),
                           ('poly', 2, 0, 5),
                           ('poly', 3, 0, 5),
                           ('rbf', 0, 2, 0),
                           ('rbf', 0, 100, 0)]:
        # Fit the model
        clf = svm.SVC(kernel=kk, degree=dd, coef0=cc, gamma=gg)
        clf.fit(X, Y)
        plot_model(X, Y, clf, fignum)
        fignum += 1
       

    

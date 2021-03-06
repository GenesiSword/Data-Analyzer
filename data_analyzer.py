"""
    The data_analyzer is an application which allows to make
    simple analyses of data saved as .csv file.

    It is based on the following sections:
    1) See your data details.
    2) Data preparation.
    3) Make visualisations.
    4) Load new data.
    5) Save your data
    6) Close the program.
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

sns.set_style('white')


def ask_for_int(demand, number=None):
    """
    Is used to check whether the entered data
    is a number.
    Arguments:
    demand: question asked to the user.
    number: entered number.
    """
    while True:
        try:
            number = int(input(demand))
        except ValueError:
            print('Give the number. ')
        else:
            return number


def ask_for_path(demandpath, path=None):
    """
    Is used to check whether the entered path
    for file is correct.
    Arguments:
    demandpath: question asked to the user.
    path: entered path.
    """
    while True:
        try:
            path = str(input(demandpath))
            os.chdir(path)
        except FileNotFoundError:
            print('Give the right path to your file.')
        else:
            return path


def ask_for_col(demandcol, col=None):
    """
    Is used to check whether the entered variable name
    is in dataframe.
    Arguments:
    demandcol: question asked to the user.
    col: entered variable name.
    """
    while True:
        try:
            col = str(input(demandcol))
            if col not in ALPHA.datafr.columns:
                raise IOError('Given variable name must be in data frame.')
        except IOError as err:
            print(str(err))
        else:
            return col


def yes_no(demandec, answer=None):
    """
    Is used to check whether the entered answer
    is "Yes" or "No".
    Arguments:
    demandpath: question asked to the user.
    answer: entered answer.
    """
    while True:
        try:
            answer = str(input(demandec))
            if answer.upper() != 'YES' and answer.upper() != 'NO':
                raise IOError("""Answer "Yes" or "No": """)
        except IOError as err:
            print(str(err))
        else:
            return answer.upper()


class Analyze:
    """
    This class allows to:
    - Save your data.
    - Load your data.
    - Create dummy variables.
    - Perform scaling.
    - Manage outliers.
    """
    def __init__(self, datafr=None):

        self.datafr = datafr

    def save(self, locs=None, datanames=None, separators=None):
        """
        Saving your data as .csv file after specifying the following
        arguments:
        locs: localization where your data will be saved
        datanames: given name of saved DataFrame. Adds .csv extension
        automatically.
        separators: separator of your DataFrame.
        """
        locs = ask_for_path('Give the path where you want' \
                            'to save your CSV file. ')
        os.chdir(locs)
        datanames = str(input('How you want to name your file? ')) + '.csv'
        separators = str(input('Give the separator of your data. '))
        self.datafr.to_csv(datanames, sep=separators)
        print('\nYour data has been saved.')

    def load(self, locl=None, datanamel=None, separatorl=None):
        """
        Loading your .csv file after specifying the following arguments:
        locl: localization of folder with your data.
        datanamel: name of your DataFrame. Adds .csv extension
        automatically.
        separatorl: separator of your DataFrame.
        """
        locl = ask_for_path('Give the path for your CSV file. ')
        os.chdir(locl)
        separatorl = str(input('Give the separator of your data. '))

        while True:
            try:
                datanamel = str(input('What is the name of file'\
                                      'with your data. '))
                self.datafr = pd.read_csv(datanamel, sep=separatorl)
            except FileNotFoundError:
                print('Give the right name of your CSV file. ')
            else:
                break

        print('\nThe head of your data: ')
        print(self.datafr.head())
        print('\nYour data has been loaded.')

    def dummies(self, numdum=None, listdum=None):
        """
        Creating  dummy variable for indicated variables.
        Arguments:
        numdum: number of variables which you want to transform
        into dummy variables.
        listdum: list of variables which will be transformed into dummy variables.
        """
        listdum = []
        numdum = ask_for_int('How many categorical variables '\
                             'your dataset has? ')
        for dummy_catvar in range(0, numdum):
            listdum.append(ask_for_col('Give the name of'\
                                       ' categorical variable: '))

        self.datafr = pd.get_dummies(self.datafr,
                                     columns=listdum,
                                     drop_first=True)

        print('\nDummy variables has been created.')

    def standscal(self,
                  scaler=None,
                  scfeat=None,
                  numsc=None,
                  listsc=None,
                  scfeatdf=None):
        """
        Allowing to perform standard scaling for indicated variables.
        For more details see "StandardScaler()".
        """
        listsc = []
        numsc = ask_for_int('How many variables you want to scale? ')
        for dummy_scalvar in range(0, numsc):
            listsc.append(ask_for_col('Give the name of variable'\
                                      ' which you want to scale: '))

        scaler = StandardScaler()
        scaler.fit(self.datafr[listsc])
        scfeat = scaler.transform(self.datafr[listsc])
        scfeatdf = pd.DataFrame(scfeat, columns=listsc)
        self.datafr[listsc] = scfeatdf[listsc]

        print('\nStandard scaling has been done.')

    def outliers(self,
                 numout=None,
                 listout=None,
                 varout=None,
                 lowqua=None,
                 upqua=None,
                 outdec=None):
        """
        Managing outliers. It allows to see outliers for indicated
        variables and decide whether user want to delete them or not.
        Arguments:
        numout: number of variables which you want to check for outliers.
        listout: list of variables which will be checked for outliers.
        varout, lowqua, upqua: arguments used for outliers detecting.
        outdec: decide whether outliers will be deletd or not.
        "Yes" for delete, "No" for not deleting.
        """
        listout = []
        numout = ask_for_int('How many variables'\
                             ' you want to check for outliers? ')

        for dummy_outnum in range(0, numout):
            listout.append(ask_for_col('Give the name of variable'\
                                       ' to be checked for outliers. '))

        for outvar in listout:
            varout = self.datafr[outvar]
            lowqua = varout.quantile(.25) - (varout.quantile(.75) -
                                             varout.quantile(.25))*1.5
            upqua = varout.quantile(.75) + (varout.quantile(.75) -
                                            varout.quantile(.25))*1.5
            print("""Variable "{}" has the following outliers: """.format(outvar))
            print('\n')
            print(self.datafr[(varout < lowqua) | (varout > upqua)])
            print('\n')

            outdec = yes_no('Do you want to delete these outliers? (Yes/No): ')

            if outdec.upper() == 'YES':

                self.datafr[outvar] = varout[varout.between(lowqua, upqua)]

                print('\nThe outliers has been deleted.')

            else:

                pass


class Visual:
    """
    Making following visualisations for loaded dataset.
    Can be performed the following visualisations:
    1) Regression
    2) Heatmap
    3) Barplot
    4) Countplot
    5) Boxplot
    6) Distribution
    7) Jointplot
    8) Pairplot
    9) Exit this section
    """
    def __init__(self, datatovis):

        self.datatovis = datatovis

    def regression(self, xdata=None, ydata=None):
        """
        See "lmplot" for seaborn.
        """
        xdata = ask_for_col('Give the name of variable for X axis. ')
        ydata = ask_for_col('Give the name of variable for Y axis. ')
        sns.lmplot(x=xdata, y=ydata, data=self.datatovis)
        plt.show()

        print('\n The plot has been created.')

    def heatmap(self):
        """
        See "heatmap" for seaborn.
        """
        sns.heatmap(data=self.datatovis, cmap='coolwarm')
        plt.show()

        print('\n The plot has been created.')

    def barplot(self, xdata=None, ydata=None):
        """
        See "barplot" for seaborn.
        """
        xdata = ask_for_col('Give the name of variable for X axis. ')
        ydata = ask_for_col('Give the name of variable for Y axis. ')
        sns.barplot(x=xdata, y=ydata, data=self.datatovis)
        plt.show()

        print('\n The plot has been created.')

    def countplot(self, xdata=None):
        """
        See "countplot" for seaborn.
        """
        xdata = ask_for_col('Give the name of variable'\
                            ' which you want to count and plot. ')
        sns.countplot(x=xdata, data=self.datatovis)
        plt.show()

        print('\n The plot has been created.')

    def boxplot(self, xdata=None, ydata=None):
        """
        See "boxplot" for seaborn.
        """
        xdata = ask_for_col('Give the name of variable to categorize data. ')
        ydata = ask_for_col('Give the name of variable for Y axis. ')
        sns.boxplot(x=xdata, y=ydata, data=self.datatovis)
        plt.show()

        print('\n The plot has been created.')

    def distribution(self, xdata=None):
        """
        See "distribution" for seaborn.
        """
        xdata = ask_for_col('Give the name of variable to plot. ')
        sns.distplot(self.datatovis[xdata])
        plt.show()

        print('\n The plot has been created.')

    def jointplot(self, xdata=None, ydata=None):
        """
        See "jointplot" for seaborn.
        """
        xdata = ask_for_col('Give the name of the first variable. ')
        ydata = ask_for_col('Give the name of the second variable. ')
        sns.jointplot(x=xdata, y=ydata, data=self.datatovis)
        plt.show()

        print('\n The plot has been created.')

    def pairplot(self):
        """
        See "pairplot" for seaborn.
        """
        sns.pairplot(data=self.datatovis)
        plt.show()

        print('\n The plot has been created.')


if __name__ == "__main__":

    print(
        """
        Welcome!

        Load your data to analyze!
        """)

    ALPHA = Analyze()
    ALPHA.load()
    BETA = Visual(ALPHA.datafr)

    while True:

        print(
            """
            Now you can choose one of these ACTIONs entering the numer before ")".

            1) See your data details.
            2) Data preparation.
            3) Make visualisations.
            4) Load new data.
            5) Save your data
            6) Close the program.

            """)

        ACTION = ask_for_int('What do you want to do? ')

        if ACTION == 1:

            print(
        """
        This is head of your data:
        {}
        
        Descriptive statistics:
        
        {}
        
        Correlation matrix:
        
        {}
        """.format(ALPHA.datafr.head(),
                   ALPHA.datafr.describe(),
                   ALPHA.datafr.corr()))

        elif ACTION == 2:

            while True:

                print("""
                        You can now perform one of these ACTIONs:
                        1) Create dummy variables.
                        2) Standarize your data.
                        3) Manage outliers.
                        4) Manage NA values.
                        5) Exit this section.
                        """)

                ACTIONPREP = ask_for_int('What do you want to do? ')

                if ACTIONPREP == 1:

                    ALPHA.dummies()

                elif ACTIONPREP == 2:

                    ALPHA.standscal()

                elif ACTIONPREP == 3:

                    ALPHA.outliers()

                elif ACTIONPREP == 4:

                    print("""You can see your NA values"""\
                          """in plot below (marked as "1")""")
                    sns.heatmap(ALPHA.datafr.isna(),
                                cmap='coolwarm',
                                linewidths=.2)
                    plt.show()

                    NADEC = str(input('Do you want to remove '\
                                      ' rowes with NA values? (Yes/No) '))

                    if NADEC.upper() == 'YES':

                        ALPHA.datafr.dropna(inplace=True)

                        print('\n NA values has been deleted.')

                    else:

                        pass

                elif ACTIONPREP == 5:

                    break

                else:
                    print('\n')
                    print('Give the number of the specific ACTION. ')

        elif ACTION == 3:

            while True:

                print(
                    """

                    This section of program allows you to make visualisations.
                    To execute specific visualisation enter the numer before ")".
                    To leave section with visualisations press "9".

                    1) Regression
                    2) Heatmap
                    3) Barplot
                    4) Countplot
                    5) Boxplot
                    6) Distribution
                    7) Jointplot
                    8) Pairplot
                    9) Exit this section.

                    """)

                CHVISUAL = ask_for_int('Which visualisation'\
                                       'you want to make? ')

                if CHVISUAL == 1:

                    BETA.regression()

                elif CHVISUAL == 2:

                    BETA.heatmap()

                elif CHVISUAL == 3:

                    BETA.barplot()

                elif CHVISUAL == 4:

                    BETA.countplot()

                elif CHVISUAL == 5:

                    BETA.boxplot()

                elif CHVISUAL == 6:

                    BETA.distribution()

                elif CHVISUAL == 7:

                    BETA.jointplot()

                elif CHVISUAL == 8:

                    BETA.pairplot()

                elif CHVISUAL == 9:

                    break

                else:
                    print('\n')
                    print('Give the number of the specific ACTION. ')

        elif ACTION == 4:

            ALPHA = Analyze()
            ALPHA.load()

        elif ACTION == 5:

            ALPHA.save()

        elif ACTION == 6:

            break

        else:
            print('\n')
            print('Give the number of the specific ACTION. ')

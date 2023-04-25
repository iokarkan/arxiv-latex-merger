import unittest
import os
import json
from .demacro import LatexDemacro

class DemacroTDD(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
            cls.sample_input = "./temp.tex"
     
    @classmethod
    def tearDownClass(cls):
        os.remove(cls.sample_input)

    def test_def_nobracket_args(self):
        with open(self.sample_input, 'w') as file:
            file.write(
r"""
\def \test [#1]{testing #1}
\test\alpha
""")
        content = LatexDemacro(self.sample_input).process()
        self.assertEqual(content,
r"""

testing \alpha
""", msg="Fails when no brackets are used, as in this example of single-arg macro.")

    ###################################################################################

    def test_def_space_after_numargs(self):
        with open(self.sample_input, 'w') as file:
            file.write(
r"""
\def \test [#1] {testing #1}
\test(\alpha)
""")
        content = LatexDemacro(self.sample_input).process()
        self.assertEqual(content,
r"""

testing \alpha
""", msg="UnboundLocalError when failing to see spaces after [#1] to find the definition.")

    ###################################################################################

    def test_def_symbol_redefinitions(self):
        with open(self.sample_input, 'w') as file:
            file.write(
r"""
\def \[ { x\[ }
$ \[ \] $
""")
        content = LatexDemacro(self.sample_input)
        content.process()
        # print(json.dumps(content.def_declarations, indent=2))
        self.assertEqual(content.tmp, 
r"""

$ x\[ \] $
""", 
    msg="""UnboundLocalError because regex for def declaration cannot understand \[ for example.
    Adding this as symbols in the current regex breaks the functionality when, e.g. \def\test[#1]{#1} is parsed,
    because then it would read the macro occurence as "test\[" and re.compile fails.
    """)


#######################################################################################


class LegaCyDemacroTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_input = "./temp.tex"

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.sample_input)

    ####################################################################################

    def test_ignore_comments(self):
        with open(self.sample_input, 'w') as file:
            file.write(
r"""
%  \newcommand\test{Testing}
\test
""")
        content = LatexDemacro(self.sample_input).process()
        self.assertEqual(content, 
r"""
\test
""")

    ####################################################################################

    def test_def_nobrackets(self):
        with open(self.sample_input, 'w') as file:
            file.write(
r"""
\def \NAS {National Academy of Science}
\NAS
""")
        content = LatexDemacro(self.sample_input).process()
        # print(content)
        self.assertEqual(content, 
r"""

National Academy of Science
""")

    ####################################################################################

    def test_newcommand_noargs(self):
        with open(self.sample_input, 'w') as file:
            file.write(
r"""
\newcommand{\test}{This is 

something to test \frac{1}{2}! 
}

\renewcommand\multi{This is 

something to test a \frac{1}{2}! 
}

\providecommand{\cultural}{This is 

something third to test \frac{1}{2} \frac{3}{4}! 
}


and some stuff in the end
\multi
\multicultural
""")
        content = LatexDemacro(self.sample_input).process()
        # print(content)
        self.assertEqual(content, 
r"""







and some stuff in the end
This is 

something to test a \frac{1}{2}! 

\multicultural
""")

    ####################################################################################

    def test_newcommand_args(self):
        with open(self.sample_input, 'w') as file:
                    file.write(
r"""
\newcommand{\name}[2]{#1 and #2}
\name{one}{two}
\names{one}{two}
""")
        content = LatexDemacro(self.sample_input).process()
        # print(content)
        self.assertEqual(content, 
r"""

one and two
\names{one}{two}
""")
                         
    ####################################################################################

    def test_newcommand_with_and_without_args(self):
        with open(self.sample_input, 'w') as file:
            file.write(
r"""
\newcommand{\test}{This is 

something to test \frac{1}{2}! 
}

\renewcommand\multi{This is 

something to test a \frac{1}{2}! 
}

\providecommand{\cultural}{This is 

something third to test \frac{1}{2} \frac{3}{4}! 
}


and some stuff in the end
\multi
\multicultural


\newcommand{\name}[2]{#1 and #2}
\name{one}{two}
\names{one}{two}
""")
        content = LatexDemacro(self.sample_input).process()
        self.assertEqual(content, 
r"""







and some stuff in the end
This is 

something to test a \frac{1}{2}! 

\multicultural



one and two
\names{one}{two}
""")

    ####################################################################################
                       
    def test_def(self):
        with open(self.sample_input, 'w') as file:
            file.write(
r"""
\def \:{\mskip .5\thinmuskip}
\def\ph {{\hbox to 0pt{\phantom{$\scriptstyle -1$}\hss}}}

\def \id{\mathop{\mathrm{id}}\nolimits}

\def\bbC {\mathbb C}

\def\pssddots (#1,#2){
  \psx #1\psxunit
  \psy #2\psyunit
}
\def\pssddotss [#1,#2]{
  \psx #1\psxunit
  \psy #2\psyunit
}

\:
\id
\ph
\bbC
\pssddots(2,3)
\pssddotss(2,3)
""")
        content = LatexDemacro(self.sample_input).process()
        self.assertEqual(content, 
r"""










\mskip .5\thinmuskip
\mathop{\mathrm{id}}\nolimits
{\hbox to 0pt{\phantom{$\scriptstyle -1$}\hss}}
\mathbb C

  \psx 2\psxunit
  \psy 3\psyunit


  \psx 2\psxunit
  \psy 3\psyunit

""")

if __name__ == 'main':
    unittest.main()
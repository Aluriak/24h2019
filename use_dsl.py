

import dsl


dsl.interpret_string("""

group 1, 2, 3 as g1.
group 4, 5, 6 as g2.

fill g1 in red.

whenever button 1 is pressed {
    color g2 in green
}
whenever button 1 is not pressed {
    color g2 in red
}

wait forever.


""")

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace, Token, Punctuation, Text


class EscsStyle(Style):
    """
    """

    background_color = "#000000"
    default_style    = "#957C8B"

    styles = {
        Token:                     "#cccccc",
        # Whitespace:                "#957C8B",
        # Note: The Text tokens are set to default_style. So, when inserting chars.
        # it gets highlighed afterwards.
        Text:                      '#957C8B',
        Comment:                   "#FF0505",
        Comment.Hashbang:          "#FF0505",
        Comment.Multiline:         "#FF0505",
        Comment.Preproc:           "#FF0505",
        Comment.Single:            "#FF0505",
        Comment.Special:           "#FF0505",

        Keyword:                   "#F7F7F0",
        # Keyword.Constant:          "",
        # Keyword.Declaration:       "#BDBD02",
        # Keyword.Namespace:         "#BDBD02",
        # Keyword.Pseudo:            "#BDBD02",
        # Keyword.Reserved:          "#BDBD02",
        # Keyword.Type:              "#BDBD02",

        Operator:                  "#F7F7F0",
        Operator.Word:             "#F7F7F0",
        Punctuation:               "#F7F7F0",

        Name:                      "#C4C4C4",
        Name.Attribute:            "#C4C4C4",
        Name.Builtin:              "#F7F7F0",
        Name.Class:                "#FCF805",
        Name.Function:             "#FCF805",
        Name.Constant:             "#C4C4C4",
        Name.Decorator:            "#C4C4C4",
        # Name.Entity:               "",
        # Name.Label:                "",
        # Name.Namespace:            "",
        # Name.Other:                "",
        # Name.Tag:                  "",
        Name.Exception:            "#C4C4C4",
        Name.Variable:             "#C4C4C4",

        String:                    "#FCF805",
        String.Single:             "#FCF805",
        String.Double:             "#FCF805",
        String.Backtick:           "#FCF805",
        String.Char:               "#FCF805",
        String.Doc:                "#FCF805",
        String.Regex:              "#FCF805",
        String.Symbol:             "#FCF805",
        Number:                    "#C4C4C4",
        
        Generic:                   "#CBCBF2",
        Generic.Heading:           "#CBCBF2",
        Generic.Subheading:        "#CBCBF2",
        Generic.Deleted:           "#cd0000",
        Generic.Inserted:          "#00cd00",
        Generic.Error:             "#FF0000",
        Generic.Emph:              "#CBCBF2",
        Generic.Strong:            "#CBCBF2",
        Generic.Prompt:            "#CBCBF2",
        Generic.Output:            "#CBCBF2",
        Generic.Traceback:         "#CBCBF2",

        Error:                     "#FF0000"
    }


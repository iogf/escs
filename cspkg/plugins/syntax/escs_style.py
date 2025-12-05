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
        Text:                      '#C4C4C4',
        Comment:                   "#FCF805",
        Comment.Hashbang:          "#FCF805",
        Comment.Multiline:         "#FCF805",
        Comment.Preproc:           "#FCF805",
        Comment.Single:            "#FCF805",
        Comment.Special:           "#FCF805",

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
        Name.Decorator:            "#FF0808",
        # Name.Entity:               "",
        # Name.Label:                "",
        # Name.Namespace:            "",
        # Name.Other:                "",
        # Name.Tag:                  "",
        Name.Exception:            "#FF0808",
        Name.Variable:             "#C4C4C4",

        String:                    "#F7F7F0",
        String.Single:             "#F7F7F0",
        String.Double:             "#F7F7F0",
        String.Backtick:           "#F7F7F0",
        String.Char:               "#F7F7F0",
        String.Doc:                "#FCF805",
        String.Regex:              "#F7F7F0",
        String.Symbol:             "#F7F7F0",
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


from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace, Token, Punctuation, Text


class StrongStyle(Style):
    """
    """

    background_color = "#000000"
    default_style    = "#957C8B"

    styles = {
        Token:                     "#cccccc",
        # Whitespace:                "#957C8B",
        # Note: The Text tokens are set to default_style. So, when inserting chars.
        # it gets highlighed afterwards.
        Text:                      '#D959FF',
        Comment:                   "#FFBCA3",
        Comment.Hashbang:          "#FFBCA3",
        Comment.Multiline:         "#FFBCA3",
        Comment.Preproc:           "#FFBCA3",
        Comment.Single:            "#FFBCA3",
        Comment.Special:           "#FFBCA3",

        Keyword:                   "#719BF0",
        # Keyword.Constant:          "",
        # Keyword.Declaration:       "#BDBD02",
        # Keyword.Namespace:         "#BDBD02",
        # Keyword.Pseudo:            "#BDBD02",
        # Keyword.Reserved:          "#BDBD02",
        # Keyword.Type:              "#BDBD02",

        Operator:                  "#719BF0",
        Operator.Word:             "#719BF0",
        Punctuation:               "#719BF0",

        Name:                      "#CCCAC8",
        Name.Attribute:            "#EDF71B",
        Name.Builtin:              "#CCCAC8",
        Name.Class:                "#EDF71B",
        Name.Function:             "#EDF71B",
        Name.Constant:             "#EDF71B",
        Name.Decorator:            "#EDF71B",
        # Name.Entity:               "",
        # Name.Label:                "",
        # Name.Namespace:            "",
        # Name.Other:                "",
        # Name.Tag:                  "",
        Name.Exception:            "#27F531",
        Name.Variable:             "#00cdcd",

        String:                    "#719BF0",
        String.Single:             "#719BF0",
        String.Double:             "#719BF0",
        String.Backtick:           "#719BF0",
        String.Char:               "#719BF0",
        String.Doc:                "#719BF0",
        String.Regex:              "#719BF0",
        String.Symbol:             "#719BF0",
        Number:                    "#B8AD89",
        
        Generic.Heading:           "#CBCBF2",
        Generic.Subheading:        "#CBCBF2",
        Generic.Deleted:           "#cd0000",
        Generic.Inserted:          "#00cd00",
        Generic.Error:             "#FF0000",
        # Generic.Emph:              "",
        # Generic.Strong:            "",
        Generic.Prompt:            "#000080",
        Generic.Output:            "#888",
        Generic.Traceback:         "#04D",

        Error:                     "#FF0000"
    }


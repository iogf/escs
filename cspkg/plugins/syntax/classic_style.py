from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace, Token, Punctuation, Text


class ClassicStyle(Style):
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
        Comment:                   "#ffbf00",
        Comment.Hashbang:          "#006680",
        Comment.Multiline:         "#807100",
        Comment.Preproc:           "#ff8000",
        Comment.Single:            "#f55600",
        Comment.Special:           "#cd0000",

        Keyword:                   "#F2F2E9",
        # Keyword.Constant:          "",
        # Keyword.Declaration:       "#BDBD02",
        # Keyword.Namespace:         "#BDBD02",
        # Keyword.Pseudo:            "#BDBD02",
        # Keyword.Reserved:          "#BDBD02",
        # Keyword.Type:              "#BDBD02",

        Operator:                  "#F2F2E9",
        Operator.Word:             "#F2F2E9",
        Punctuation:               "#F2F2E9",

        Name:                      "#C7C7C3",
        Name.Attribute:            "#C7C7C3",
        Name.Builtin:              "#C7C7C3",
        Name.Class:                "#FCF805",
        Name.Function:             "#FCF805",
        Name.Constant:             "",
        Name.Decorator:            "#8B8B6E",
        # Name.Entity:               "",
        # Name.Label:                "",
        # Name.Namespace:            "",
        # Name.Other:                "",
        # Name.Tag:                  "",
        Name.Exception:            "#666699",
        Name.Variable:             "#00cdcd",

        String:                    "#D4A59B",
        String.Single:             "#D4A59B",
        String.Double:             "#D4A59B",
        String.Backtick:           "#ADAAAA",
        String.Char:               "#ADAAAA",
        String.Doc:                "#719BF0",
        String.Regex:              "#ADAAAA",
        String.Symbol:             "#BFBF6B",
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


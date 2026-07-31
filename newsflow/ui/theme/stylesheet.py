from newsflow.ui.theme.colors import Colors


def application_stylesheet() -> str:

    return f"""

    QWidget {{
        background-color: {Colors.BACKGROUND};
        color: {Colors.TEXT};
        font-family: "Segoe UI";
        font-size: 14px;
    }}

    QLabel {{
        color: {Colors.TEXT};
        background: transparent;
    }}

    #CardWidget {{

        background-color: {Colors.CARD};

        border: 1px solid {Colors.BORDER};

        border-radius: 14px;

    }}

    #CardWidget:hover {{

        background-color: {Colors.CARD_HOVER};

        border: 1px solid {Colors.PRIMARY};

    }}

    QPushButton {{

        background:qlineargradient(

            x1:0,

            y1:0,

            x2:1,

            y2:0,

            stop:0 #8A2BE2,

            stop:1 #D946EF

        );

        border:none;

        border-radius:10px;

        color:white;

        font-weight:bold;

        padding:12px;

        min-height:24px;

    }}

    QPushButton:hover {{

        background:qlineargradient(

            x1:0,

            y1:0,

            x2:1,

            y2:0,

            stop:0 #9F43FF,

            stop:1 #F15BFF

        );

    }}

    QPushButton:pressed {{

        background:#7D1FD3;

    }}

    QListWidget {{

        background-color:{Colors.INPUT};

        border:1px solid {Colors.BORDER};

        border-radius:8px;

    }}

    QLineEdit,
    QTextEdit,
    QPlainTextEdit {{

        background-color:{Colors.INPUT};

        border:1px solid {Colors.BORDER};

        border-radius:8px;

        padding:8px;

    }}

    """
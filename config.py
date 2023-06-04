
# Windows Path
LISTEN_PATH = 'E:\\Descargas\\Demo2\\'

# Linux Path
# LISTEN_PATH = "/home/<USER>/Downloads/"



# Directory config
SOUND_DIR_NAME = "sound"
VIDEO_DIR_NAME = "video"
DOCS_DIR_NAME = "docs"
PRESENTATION_DIR_NAME = "presentations"
SPREADSHEETS_DIR_NAME = "spreadsheets"
DOCUMENTS_DIR_NAME = "documents"
COMPRESSED_DIR_NAME = "compress"
SYSTEMS_DIR_NAME = "isos"
BINARIES_DIR_NAME = "binaries"
IMAGES_DIR_NAME = "images"
CODE_DIR_NAME = "code"

BASE_STRUCTURE = {
    CODE_DIR_NAME: [
        "java",
        "js",
        "ts",
        "html",
        "xml",
        "css",
        "py"
    ],
    SOUND_DIR_NAME: [
        "mp3",
        "wav",
        "wma",
        "m4a",
        "aac",
        "aa"
    ],
    VIDEO_DIR_NAME: [
        "mkv",
        "mp4",
        "mpg",
        "mov",
        "webm",
        "avi",
        "flv",
        "mpeg",
        "ogg",
        "wmv"
    ],
    DOCS_DIR_NAME: {
        PRESENTATION_DIR_NAME: [
            "opd",
            "otp",
            "pot",
            "potm",
            "potx",
            "pps",
            "ppsm",
            "ppsx",
            "ppt",
            "pptx",
            "pptm"
        ],
        SPREADSHEETS_DIR_NAME: [
            "xls",
            "csv",
            "dif",
            "ods",
            "xlm",
            "ots"
        ],
        DOCUMENTS_DIR_NAME: [
            "txt",
            "docx",
            "pdf",
            "odt",
            "doc"
        ] 
    },
    IMAGES_DIR_NAME: [
        "png",
        "jpeg",
        "jpg",
        "gif",
        "tif",
        "tiff",
        "bmp",
        "eps",
        "psd",
        "ai",
        "raw",
        "svg",
        "webp",
        "ico"
    ],
    BINARIES_DIR_NAME: [
        "exe",
        "bin"
    ],
    SYSTEMS_DIR_NAME: [
        "iso",
        "img"
    ],
    COMPRESSED_DIR_NAME: [
        "rar",
        "zip",
        "gz",
        "tar"
    ]
}
# -------------------------------------------------
# Project created by QtCreator 2009-04-20T18:42:44
# -------------------------------------------------
QT += core \
    gui
TARGET = growlnotification
TEMPLATE = lib
CONFIG += qt \
    plugin
INCLUDEPATH += ../../include
DESTDIR = build
QMAKE_LFLAGS += -framework \
    Growl \
    -framework \
    CoreFoundation
FORMS += ui/settings.ui
HEADERS += src/notifyhelper.h \
    src/growlsettings.h \
    src/growlnotificationlayer.h \
    src/growlnotificationcore.h \
    src/growlnotification.h
SOURCES += src/notifyhelper.cpp \
    src/growlsettings.cpp \
    src/growlnotificationlayer.cpp \
    src/growlnotificationcore.cpp \
    src/growlnotification.cpp
RESOURCES += growlnotification.qrc
UI_DIR = ui

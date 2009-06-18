#ifndef H_GROWLSOUND
#define H_GROWLSOUND
#include <QObject>


class GrowlSound
{
public:
    GrowlSound();
    ~GrowlSound();
    void PlaySound(const QString &);

private:
    class Private;
    Private * d;
};
#endif

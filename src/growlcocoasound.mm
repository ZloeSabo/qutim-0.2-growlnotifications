#include <Cocoa/Cocoa.h>

#include "growlcocoasound.h"

class GrowlSound::Private
{
        public:
                NSAutoreleasePool* autoReleasePool_;
};

GrowlSound::GrowlSound() {
    this->d = new Snd::Private;
    NSApplicationLoad();
    d->autoReleasePool_ = [[NSAutoreleasePool alloc] init];
}

GrowlSound::~GrowlSound() {
    [d->autoReleasePool_ release];
    delete d;
}

void GrowlSound::PlaySound(const QString & soundfile)
{
	NSSound *sound = [[NSSound alloc]
					  initWithContentsOfFile: 
                                          [NSString stringWithUTF8String: soundfile.toUtf8().data()]
					  byReference: YES];
	[sound play];
}

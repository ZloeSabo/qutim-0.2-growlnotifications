/*
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */

#ifndef GROWLNOTIFICATIONCORE_H
#define GROWLNOTIFICATIONCORE_H
#include <qutim/plugininterface.h>
#include <qutim/layerinterface.h>
#include "growlnotificationlayer.h"
#include "growlnotification.h"
#include <QIcon>
//#include <QWidget>

using namespace qutim_sdk_0_2;

class GrowlNotificationCore : public QObject, public LayerPluginInterface//, public SimplePluginInterface
{
        Q_OBJECT
	Q_INTERFACES(qutim_sdk_0_2::PluginInterface)
public:
        virtual bool init(PluginSystemInterface* plugin_system);
	
	virtual void release();
        virtual void processEvent(PluginEvent &event);
	virtual void setProfileName(const QString &profileName);
	virtual QString name();
	virtual QString description();
        //virtual QString type();
        virtual QIcon *icon();

private slots:

private:
        QIcon *GrowlNotificationIcon;
        PluginSystemInterface *GrowlNotificationPluginSystem;
	QString m_profile_name;
        GrowlNotificationLayer *m_notification_layer;
};

#endif // GROWLNOTIFICATIONCORE_H

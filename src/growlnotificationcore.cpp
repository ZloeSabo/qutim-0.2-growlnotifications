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

#include <QDebug>
#include "growlnotificationcore.h"
#include "growlnotification.h"

/*
* @brief initializes core. also there is the best place to assign your layer
* @param plugin_system is QutIM plugin system, used here to interact and assign layer interface
*/
bool GrowlNotificationCore::init(PluginSystemInterface *plugin_system)
{
        PluginInterface::init(plugin_system);
        GrowlNotificationIcon = new QIcon(":/ico/GrowlAlert.png");
        GrowlNotificationPluginSystem = plugin_system;

        //Whatever this is needed for...
        this->m_notification_layer = new GrowlNotificationLayer ();
        this->m_notification_layer->registerPluginSystem(GrowlNotificationPluginSystem);
        
        GrowlNotificationPluginSystem->setLayerInterface (NotificationLayer , this->m_notification_layer);
        qDebug() << "GrowlNotification: core initialized";

        return true;
}

/*
* @brief release whatever
*/
void GrowlNotificationCore::release()
{
    //TODO:release something
}

void GrowlNotificationCore::processEvent(PluginEvent &event)
{
}

/*
* @brief plugin name. Didn't find any sign if QutIM uses it.
*/
QString GrowlNotificationCore::name()
{
        return "GrowlNotification";
}

/*
* @brief plugin description. Didn't find any sign if QutIM uses it.
*/
QString GrowlNotificationCore::description()
{
        return "Growl notification plugin";
}

/*
* @brief plugin icon. Didn't find any sign if QutIM uses it.
*/
QIcon *GrowlNotificationCore::icon()
{
        return this->GrowlNotificationIcon;
}

/*
*@brief One of functions needed by interface. Could be copied as is
*/
void GrowlNotificationCore::setProfileName(const QString &profileName)
{
        m_profile_name = profileName;
}

Q_EXPORT_PLUGIN2(GrowlNotificationCore, GrowlNotificationCore);

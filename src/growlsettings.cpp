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

#include "growlsettings.h"
#include <QString>
#include <QVariant>

//Whatever is that for, but static methods don't work without such initialisation
QSettings * GrowlSettings::settings;

/*
* \brief Loads config file. Needs to be invoked only once
* \param profile_name name of user profile. usually could be taken from setProfileName or so on
*/
void GrowlSettings::load(const QString & profile_name)
{
    GrowlSettings::settings  = new QSettings(QSettings::IniFormat, QSettings::UserScope, "qutim/qutim."+profile_name, "plugin_growl");
}

/*
* \brief returns value of given parameter
* \param name name of the parameter you need
*/
const QVariant GrowlSettings::value(const QString & name)
{
    QVariant val = settings->value(name, false);
    return val;
}

/*
* \brief checks if parameter is set in config file
* \param name name of the parameter you need
*/
const bool GrowlSettings::isValid(const QString & name)
{
    bool ret = settings->contains(name);
    return ret;
}

/*
* \brief sets value of given parameter and flushes changes in config file
* \param key name of the parameter you need
* \param value value of the parameter with name stored in key
*/
void GrowlSettings::setValue(const QString & key, const QVariant & value)
{
    settings->setValue(key, value);
    settings->sync();
}

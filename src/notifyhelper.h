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

#ifndef NOTIFYHELPER_H
#define NOTIFYHELPER_H

#include <QObject>
#include <qutim/plugininterface.h>
#include "growlnotification.h"

using namespace qutim_sdk_0_2;

class NotifyHelper : public QObject
{
	Q_OBJECT
public:
	NotifyHelper (const TreeModelItem &tree_model_item, PluginSystemInterface* plugin_system);
private: 	
	TreeModelItem m_contact_item;
	PluginSystemInterface *m_plugin_system;
public slots:
        void actionFilter (uint index);
        void startChatSlot ();
        void closeSlot();
        void timeoutSlot() {}; //use empty function to avoid tons of warnings in console
};
#endif // NOTIFYHELPER_H

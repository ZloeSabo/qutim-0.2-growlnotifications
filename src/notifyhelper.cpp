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
#include "notifyhelper.h"


NotifyHelper::NotifyHelper(const TreeModelItem& tree_model_item, PluginSystemInterface* plugin_system) {
        m_plugin_system = plugin_system;
        m_contact_item = tree_model_item;
}

//Unknown
void NotifyHelper::actionFilter(uint index) {
        qDebug()<< "action: "+index;

        switch (index)
        {
                case 1:
                        startChatSlot();
                        break;
                case 2:
                        closeSlot();
                        break;
                default:
                        return;
                        break;
        }
}

/*
* @brief Open chat with contact
*/
void NotifyHelper::startChatSlot() {
        m_plugin_system->createChat(m_contact_item);
        qDebug()<< "Start chat slot with " << m_contact_item.m_account_name << m_contact_item.m_item_history ;
}

/*
* @brief Close notifier window
*/
void NotifyHelper::closeSlot() {

}

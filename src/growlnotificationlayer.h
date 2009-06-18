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

#ifndef GROWLNOTIFICATIONLAYER_H
#define GROWLNOTIFICATIONLAYER_H
#include <qutim/layerinterface.h>
#include <qutim/plugininterface.h>
#include "growlnotification.h"
#include "growlsettings.h"
#include "growlcocoasound.h"
#include "ui_settings.h"

typedef QHash<QString,  bool> ActiveNotifications;
typedef QHash<QString, QCheckBox *> MenuMapping;

using namespace qutim_sdk_0_2;

class GrowlNotificationLayer : public QObject, public NotificationLayerInterface
{
    Q_OBJECT
public:
    GrowlNotificationLayer ();
    virtual ~GrowlNotificationLayer ();
    virtual bool init(PluginSystemInterface *plugin_system);
    virtual void release() {}
    virtual void removeGuiLayerSettings() {}
    virtual void removeLayerSettings();
    virtual void saveGuiSettingsPressed() {}
    virtual void saveLayerSettings();
    virtual void setLayerInterface(LayerType type, LayerInterface* interface) {}
    virtual void setProfileName(const QString& profile_name);
    virtual void systemMessage(const TreeModelItem &item, const QString &message);
    virtual void userMessage(const TreeModelItem &item, const QString &message, NotificationType type);
    void registerPluginSystem (PluginSystemInterface* plugin_system);
    virtual QList<SettingsStructure> getLayerSettingsList();

    //0.2beta
    virtual void showPopup(const TreeModelItem &item, const QString &message, NotificationType type);
    virtual void playSound(const TreeModelItem &item, NotificationType type);
    virtual void notify(const TreeModelItem &item, const QString &message, NotificationType type) { showPopup(item,message, type); };

private:
    PluginSystemInterface *m_plugin_system;
    ActiveNotifications m_activenotifications;
    MenuMapping m_mapping;
    GrowlNotifier * m_notifier;
    GrowlSettings * m_settings;
    bool m_enabled;
    Ui::GrowlSettings ui;
    QList<SettingsStructure> m_widgets;
    QWidget m_widget;
    GrowlSound sound;
private slots:
    void createDefaultIni();
};

#endif // GROWLNOTIFICATIONLAYER_H


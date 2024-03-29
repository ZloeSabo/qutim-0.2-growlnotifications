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
#include <QStringList>
#include <QMutableHashIterator>
#include <QPixmap>
#include <QFile>
#include <QFileDialog>
#include "growlnotificationlayer.h"
#include "notifyhelper.h"
#include "ui_settings.h"
/*
* @brief constructor, creates eventName - isEnabled pairs
*/
GrowlNotificationLayer::GrowlNotificationLayer ()
{
    this->m_activenotifications["Enabled"] = true;
    this->m_activenotifications["Status change"] = false;
    this->m_activenotifications["Message recieved"] = true;
    this->m_activenotifications["Contact is typing"] = false;
    this->m_activenotifications["Message blocked"] = false;
    this->m_activenotifications["Custom message"] = true;
    this->m_activenotifications["Contact came online"] = false;
    this->m_activenotifications["Contact came offline"] = false;
    this->m_activenotifications["Starting"] = false;
    this->m_activenotifications["Contact has birthday"] = false;
    this->m_activenotifications["System notification"] = false;

    this->m_button_mapper = new QSignalMapper(this);
}

GrowlNotificationLayer::~GrowlNotificationLayer ()
{
    this->m_button_mapper->~QSignalMapper();
}

bool GrowlNotificationLayer::init(PluginSystemInterface *plugin_system)
{
        Q_UNUSED(plugin_system);

        qDebug() << "GrowlNotification: layer initialized";

        return true;
}

void GrowlNotificationLayer::systemMessage(const TreeModelItem &item, const QString &message)
{
    qDebug() << "GrowlNotification: recieved system message \r\n" << message;

    this->m_notifier->notify("System notification", tr("QutIM message"), message, QPixmap(), false, this, 0, 0);
}

void GrowlNotificationLayer::userMessage(const TreeModelItem &item, const QString &message, NotificationType type)
{
        QStringList contact_info = m_plugin_system->getAdditionalInfoAboutContact(item);
        QString contact_nick = 	item.m_item_name;
        QString n_type; // notification type
        QString msg; //formatted message
        QPixmap avatar;

        if ( contact_info.count() > 0)  {
                contact_nick = contact_info.at(0);
        }

        if( contact_info.count() > 1)  {
            avatar = QPixmap(contact_info.at(1));
        }  else  {
            avatar = QPixmap();
        }

        switch ( type )  {
                case NotifyStartup:
                        msg = QObject::tr("%1").arg("Starting");
                        n_type = "Starting";
                        break;
                case NotifyCount:
                        msg = QObject::tr("%1").arg(message);
                        n_type = "NotifyCount";
                        break;
                case NotifyStatusChange:
                        msg = QObject::tr("%1").arg(message);
                        n_type = "Status change";
                        break;
                case NotifyMessageGet:
                        msg = QObject::tr("%1").arg(message);
                        n_type = "Message recieved";
                        break;
                case NotifyTyping:
                        msg = QObject::tr("Typing");
                        n_type = "Contact is typing";
                        break;
                case NotifyBlockedMessage:
                        msg = QObject::tr("Blocked message : %1").arg(message);
                        n_type = "Message blocked";
                        break;
                case NotifyBirthday:
                        msg = QObject::tr("has birthday today!!");
                        n_type = "Contact has birthday";
                        break;
                case NotifyCustom:
                        msg = QObject::tr("%1").arg(message);
                        n_type = "Custom message";
                        break;
                case NotifyOnline:
                        msg = QObject::tr("%1").arg(message);
                        n_type = "Contact came online";
                        break;
                case NotifyOffline:
                        msg = QObject::tr("%1").arg(message);
                        n_type = "Contact came offline";
                        break;
                default:
                        //msg = contact_nick + "<br />" + message;
                        //msg = QObject::tr("%1").arg(message);
                        //n_type = "Message recieved";
                        break;
        }

        if(this->m_enabled)  {
            if(this->m_settings->value(QString("main/" + n_type)).toBool())  {

                NotifyHelper *notify_helper = new NotifyHelper (item,m_plugin_system);
                this->m_notifier->notify(n_type, contact_nick, msg, avatar, false, notify_helper, SLOT(startChatSlot()), SLOT(timeoutSlot()));
                //notify_helper->deleteLater();
            }
        }

        qDebug() << "GrowlNotification: recieved message " <<contact_nick << " "<< message << " " << type;

}

void GrowlNotificationLayer::setProfileName(const QString& profile_name)
{
    qDebug() << "GrowlNotification: loading settings";
    this->m_settings = new GrowlSettings;
    this->m_settings->load(profile_name);

    //Check, if growl notifications are enabled and if so will load settings
    if (this->m_settings->isValid(QString("main/enabled"))) {
       this->m_enabled = this->m_settings->value(QString("main/enabled")).toBool();
       //if notifications are enabled...
       if(this->m_enabled)  {
           qDebug() << "GrowlNotification: notifications enabled";

           //As we cannot dispose growlnotification, we will register all the notifications and filter them later
           QMutableHashIterator<QString, bool> i(this->m_activenotifications);
           QStringList list;
           while (i.hasNext()) {
               i.next();
               if(i.key() != "Enabled")  {
                   list << i.key();
               }
               QString iniValue = "main/" + i.key();
               if(this->m_settings->isValid(iniValue))  {
                   i.value() = this->m_settings->value(iniValue).toBool(); //load settings
                   if(this->m_mapping.contains(i.key()))  {
                        this->m_mapping[i.key()]->setChecked(i.value());
                   }
               }
           }
           this->m_notifier = new GrowlNotifier(list, list, "QutIM");

           qDebug() << "GrowlNotification: notifications are enabled and have been loaded";
       }
   } else  {
       //create ini file with default values
       this->createDefaultIni();
   }
    //end settings loading
}

void GrowlNotificationLayer::registerPluginSystem (PluginSystemInterface* plugin_system)
{
        this->m_plugin_system = plugin_system;
}

void GrowlNotificationLayer::createDefaultIni()
{
    this->m_settings->setValue(QString("main/enabled"), true);
    QMutableHashIterator<QString, bool> i(this->m_activenotifications);
    while (i.hasNext())  {
        i.next();
        this->m_settings->setValue(QString("main/" + i.key()), i.value());
    }
    qDebug() << "GrowlNotification: default settings file has been generated";
}
/*
** @brief invoked to return qlist with menu item and qwidget for main settings window
*/
QList<SettingsStructure> GrowlNotificationLayer::getLayerSettingsList()
{
        SettingsStructure ss;
        ss.settings_item = new QTreeWidgetItem();
        ss.settings_item->setText(0, tr("Growl"));
        ss.settings_item->setIcon(0, QIcon(":/ico/GrowlAlert.png"));
        QWidget * widget = new QWidget;
        this->ui.setupUi(widget);

        //don't say a word...
        this->m_mapping["Status change"] = ui.StatusChange;
        this->m_mapping["Message recieved"] = ui.MessageRecieved;
        this->m_mapping["Contact is typing"] = ui.Typing;
        this->m_mapping["Message blocked"] = ui.Blocked;
        this->m_mapping["Custom message"] = ui.Custom;
        this->m_mapping["Contact came online"] = ui.ShowOnline;
        this->m_mapping["Contact came offline"] = ui.ShowOffline;
        this->m_mapping["Contact has birthday"] = ui.Birthday;
        this->m_mapping["Enabled"] = ui.NotifyEnabled;

        this->m_line_edit_mapping["startupSet"] = ui.StartupFilename;
        this->m_line_edit_mapping["syseventSet"] = ui.SystemEventFilename;
        this->m_line_edit_mapping["inSet"] = ui.IncomingFilename;
        this->m_line_edit_mapping["outSet"] = ui.OutgoingFilename;
        this->m_line_edit_mapping["onlineSet"] = ui.OnlineFilename;
        this->m_line_edit_mapping["offlineSet"] = ui.OfflineFilename;
        this->m_line_edit_mapping["statuschangeSet"] = ui.StatusChangeFilename;
        this->m_line_edit_mapping["birthdaySet"] = ui.BirthdayFilename;

        QMutableHashIterator<QString, bool> i(this->m_activenotifications);
        while (i.hasNext()) {
            i.next();
            QString iniValue = "main/" + i.key();
            if(this->m_settings->isValid(iniValue))  {
                i.value() = this->m_settings->value(iniValue).toBool(); //load settings
                if(this->m_mapping.contains(i.key()))  {
                       this->m_mapping[i.key()]->setChecked(this->m_settings->value(iniValue).toBool());
                }
             }
        }

        //Read settings for sound notifications
        QMutableHashIterator<QString, QLineEdit *> it(this->m_line_edit_mapping);
        while(it.hasNext()) {
            it.next();
            QString iniValue = "sound/" + it.key();
            if(this->m_settings->isValid(iniValue))  {
                if(this->m_line_edit_mapping.contains(it.key()))  {
                       this->m_line_edit_mapping[it.key()]->setText(this->m_settings->value(iniValue).toString());
                       //qDebug() << "set :" << i.key() <<" = " << this->m_settings->value(iniValue).toString();
                }
             }
        }

        //Mapbutton clicked event to mapper
        quint16 rows = ui.gridLayout->rowCount();
        for(quint16 num=2; num < rows; num++) {
            QLayoutItem * wid = ui.gridLayout->itemAtPosition(num, 2);
            if(!wid->isEmpty()) {
                QWidget * button = wid->widget();
                QObject::connect(button, SIGNAL(clicked()), this->m_button_mapper, SLOT(map()));
                this->m_button_mapper->setMapping(button, button->objectName());
            }
        }

        QObject::connect(this->m_button_mapper, SIGNAL(mapped(const QString &)), SLOT(fileSelectPresed(const QString &)));

        ss.settings_widget = widget;
        QList<SettingsStructure> list;
        list.append(ss);
        return list;

}

void GrowlNotificationLayer::saveLayerSettings()
{
    qDebug() << "GrowlNotification: saving settings";
    QHashIterator<QString, QCheckBox *> i(this->m_mapping);
    while(i.hasNext())  {
        i.next();
        this->m_settings->setValue("main/" + i.key(), i.value()->isChecked());
    }
    this->m_enabled = this->ui.NotifyEnabled->isChecked();

    QMutableHashIterator<QString, QLineEdit *> it(this->m_line_edit_mapping);
    while(it.hasNext())  {
        it.next();
        if(QFile::exists(it.value()->text())) {
            this->m_settings->setValue("sound/" + it.key(), it.value()->text());
        } else {
            this->m_settings->setValue("sound/" + it.key(), "");
        }
        qDebug() << "sound/" << it.key() <<" = " << it.value()->text();
    }
    //this->m_settings->setValue("main/enabled", this->ui.NotifyEnabled->isChecked());
}

//Invoked in any case in 0.2 =(
void GrowlNotificationLayer::removeLayerSettings()
{
    qDebug() << "GrowlNotification: settings change aborted";
    this->saveLayerSettings();
}

//0.2+ section
void GrowlNotificationLayer::showPopup(const TreeModelItem &item, const QString &message, NotificationType type)
{
    this->userMessage(item, message, type);
}

void GrowlNotificationLayer::playSound(const TreeModelItem &item, NotificationType type)
{
    QString n_type = "";
    switch ( type )  {
                case NotifyStartup:
                        n_type = "startupSet";
                        break;
                case NotifyStatusChange:
                        n_type = "statuschangeSet";
                        break;
                case NotifyMessageGet:
                        n_type = "inSet";
                        break;
                case NotifyMessageSend:
                        n_type = "outSet";
                        break;
                case NotifyBirthday:
                        n_type = "birthdaySet";
                        break;
                case NotifyCustom:
                        n_type = "syseventSet";
                        break;
                case NotifyOnline:
                        n_type = "onlineSet";
                        break;
                case NotifyOffline:
                        n_type = "offlineSet";
                        break;
                default:
                        break;
        }
    if(this->m_enabled && n_type != "")  {
        QString fileName = this->m_settings->value("sound/" + n_type).toString();
        if(QFile::exists(fileName))  {
            this->m_sound.PlaySound(fileName);
        }
    }
}

void GrowlNotificationLayer::fileSelectPresed(const QString &itemName)
{
    qDebug() <<  "GrowlNotification: pressed:" << itemName;
    QString oldpath = this->m_line_edit_mapping[itemName]->text();
    qDebug() << oldpath;
    if(!QFile::exists(oldpath)) {
        oldpath = QDir::homePath();
    } else {
        oldpath = QDir(oldpath).filePath(oldpath);
    }
    QString fileName = QFileDialog::getOpenFileName(&this->m_widget,
        tr("Select sound file"), oldpath,
        tr("All files (*.*)"));
    this->m_settings->setValue("sound/" + itemName, fileName);
    this->m_line_edit_mapping[itemName]->setText(fileName);
}

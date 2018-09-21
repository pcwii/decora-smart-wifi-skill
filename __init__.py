#!/usr/bin/env python
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import re
from decora_wifi import DecoraWiFiSession
from decora_wifi.models.residential_account import ResidentialAccount


__author__ = 'PCWii'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)


# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class DecoraWifiSkill(MycroftSkill):


    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(DecoraWifiSkill, self).__init__(name="DecoraWifiSkill")

        self.settings["email"] = ""
        self.settings["password"] = ""
        self.session = ""
        self.perms = []
        self._is_setup = False

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        # Check and then monitor for credential changes
        self.settings.set_changed_callback(self.on_websettings_changed)
        self.on_websettings_changed()


        decora_light_on_intent = IntentBuilder("DecoraWifiOnIntent").\
            require("DeviceKeyword").require("OnKeyword").\
            optionally("LightKeyword").\
            optionally("SilentKeyword").build()
        self.register_intent(decora_light_on_intent, self.handle_decora_light_on_intent)

        decora_light_off_intent = IntentBuilder("DecoraWifiOffIntent").\
            require("DeviceKeyword").require("OffKeyword").\
            optionally("LightKeyword").\
            optionally("SilentKeyword").build()
        self.register_intent(decora_light_off_intent, self.handle_decora_light_off_intent)

        decora_light_dim_intent = IntentBuilder("DecoraWifiDimIntent").\
            require("DimKeyword").require("DeviceKeyword").\
            optionally("LightKeyword").\
            optionally("SilentKeyword").build()
        self.register_intent(decora_light_dim_intent, self.handle_decora_light_dim_intent)

        decora_light_set_intent = IntentBuilder("DecoraWifiSetIntent").\
            require("SetKeyword").require("DeviceKeyword").\
            optionally("LightKeyword").\
            optionally("SilentKeyword").build()
        self.register_intent(decora_light_set_intent, self.handle_decora_light_set_intent)

    def on_websettings_changed(self):
        if not self._is_setup:
            email = self.settings.get("email", "")
            password = self.settings.get("password", "")
            try:
                if email and password:
                    email = self.settings["email"]
                    password = self.settings["password"]
                    self.session = DecoraWiFiSession()
                    self.session.login(email, password)
                    self.perms = self.session.user.get_residential_permissions()
                    self._is_setup = True
            except Exception as e:
                LOG.error(e)

    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.
    def handle_decora_light_on_intent(self, message):
        silent_kw = message.data.get("SilentKeyword")
        for permission in self.perms:
            acct = ResidentialAccount(self.session, permission.residentialAccountId)
            residences = acct.get_residences()
            for residence in residences:
                switches = residence.get_iot_switches()
                for switch in switches:
                    my_switch = switch
                    break
                break
            break
        my_switch.update_attributes({'power': 'ON', 'brightness': '100'})
        if not silent_kw:
            self.speak_dialog("light.on")

    def handle_decora_light_off_intent(self, message):
        silent_kw = message.data.get("SilentKeyword")
        for permission in self.perms:
            acct = ResidentialAccount(self.session, permission.residentialAccountId)
            residences = acct.get_residences()
            for residence in residences:
                switches = residence.get_iot_switches()
                for switch in switches:
                    my_switch = switch
                    break
                break
            break
        my_switch.update_attributes({'power': 'OFF'})
        if not silent_kw:
            self.speak_dialog("light.off")

    def handle_decora_light_dim_intent(self, message):
        silent_kw = message.data.get("SilentKeyword")
        for permission in self.perms:
            acct = ResidentialAccount(self.session, permission.residentialAccountId)
            residences = acct.get_residences()
            for residence in residences:
                switches = residence.get_iot_switches()
                for switch in switches:
                    my_switch = switch
                    break
                break
            break
        my_switch.update_attributes({'brightness': '5'})
        if not silent_kw:
            self.speak_dialog("light.dim")

    def handle_decora_light_set_intent(self, message):
        silent_kw = message.data.get("SilentKeyword")
        str_remainder = str(message.utterance_remainder())
        dim_level = re.findall('\d+', str_remainder)
        if dim_level:
            for permission in self.perms:
                acct = ResidentialAccount(self.session, permission.residentialAccountId)
                residences = acct.get_residences()
                for residence in residences:
                    switches = residence.get_iot_switches()
                    for switch in switches:
                        my_switch = switch
                        break
                    break
                break
            my_switch.update_attributes({'brightness': dim_level[0]})
            if not silent_kw:
                self.speak_dialog("light.set", data={"result": str(dim_level[0])+ ", percent"})

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return DecoraWifiSkill()

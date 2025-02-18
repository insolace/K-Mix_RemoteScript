from _Framework.ModeSelectorComponent import ModeSelectorComponent
from .ConfigurableButtonElement import ConfigurableButtonElement
from .K_MixUtility import K_MixUtility
from .MIDI import *

class VUModeSelector(ModeSelectorComponent, K_MixUtility):
	"""Class that selects between modes"""

	def __init__(self,mixer):
		ModeSelectorComponent.__init__(self)
		self._mixer = mixer
		self.set_mode_toggle(self.button(CHANNEL,VU_BUTTON))
		#self.update()
		

	def set_modes_buttons(self, buttons):
		#raise buttons == None or isinstance(buttons, tuple) or len(buttons) == self.number_of_modes() or AssertionError
		identify_sender = True
		for button in self._modes_buttons:
			button.remove_value_listener(self._mode_value)
			button.remove_value_listener(self._mode_release)
		self._modes_buttons = []
		if buttons != None:
			for button in buttons:
				#raise isinstance(button, ButtonElement) or AssertionError
				self._modes_buttons.append(button)
				button.add_value_listener(self._mode_value, identify_sender)
				button.add_value_listener(self._mode_release, identify_sender)
		self.set_mode(0)


	def set_mode_toggle(self, button):
		#if not (button == None or isinstance(button, ConfigurableButtonElement)):
		#	raise AssertionError
		if self._mode_toggle != None:
			self._mode_toggle.remove_value_listener(self._toggle_value)
			#self._mode_toggle.remove_value_listener(self._mode_release)
		self._mode_toggle = button
		self._mode_toggle != None and self._mode_toggle.add_value_listener(self._toggle_value)
		#self._mode_toggle.add_value_listener(self._mode_release)
		self.set_mode(0)

	def number_of_modes(self):
		return 2

	def on_enabled_changed(self):
		self.update()
	'''	
	def set_mode(self, mode):
		if mode < self.number_of_modes():
			self._mode_index = mode
			self.update()
	'''
	def update(self):
		super(VUModeSelector, self).update()
	
	def on_selected_track_changed(self):
		track =  self.song().view.selected_track
		device_count = track.devices
		'''
		if len(device_count) != 0:
			if self._device.selected_device != self.song().view.selected_track.devices[0]: 
				self.song().view.select_device(self.song().view.selected_track.devices[0])
				#self._device.selected_device = self.song().view.selected_track.devices[0]
			self._mixer.on_selected_track_changed()
		else:
			self._mixer.on_selected_track_changed()
		'''
		self._mixer.on_selected_track_changed()

	def _toggle_value(self, value):
		index = self._mode_index
		if self._mixer.is_active == True:
			if value != 0:
				if index == 0:
					self.set_mode(1)
					self._mixer.VU_mode = 1
				if index == 1:
					self.set_mode(0)
					self._mixer.VU_mode = 0
				self._mixer.setup_sliders()
		if value == 0:
			if index == 1:
				self._mode_toggle.send_value(1)

	def _mode_release(self, value):
		if value == 0:
			index = self._mode_index
			if index == 1:
				self._mode_toggle.send_value(1)
      
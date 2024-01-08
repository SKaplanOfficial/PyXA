import PyXA
import time
import unittest

import ScriptingBridge

from PyXA.apps.Music import *

class TestMusic(unittest.TestCase):
    def setUp(self):
        self.app = PyXA.Application("Music")

    def test_music_application_type(self):
        app2 = PyXA.Music()
        self.assertEqual(self.app, app2)
        self.assertIsInstance(self.app, XAMusicApplication)

    def test_music_application_attributes(self):
        self.assertIsInstance(self.app.airplay_enabled, bool)
        self.assertIsInstance(self.app.current_airplay_devices, XAMusicAirPlayDeviceList)
        self.assertIsInstance(self.app.current_encoder, XAMusicEncoder)
        self.assertIsInstance(self.app.current_eq_preset, XAMusicEQPreset)
        self.assertIsInstance(self.app.current_visual, XAMusicVisual)
        self.assertIsInstance(self.app.eq_enabled, bool)
        self.assertIsInstance(self.app.shuffle_enabled, bool)
        self.assertIsInstance(self.app.shuffle_mode, XAMusicApplication.ShuffleMode)
        self.assertIsInstance(self.app.song_repeat, XAMusicApplication.RepeatMode)
        self.assertIsInstance(self.app.visuals_enabled, bool)
        self.assertIsInstance(self.app.current_track, XAMusicTrack)

        self.assertIsInstance(self.app.airplay_devices(), XAMusicAirPlayDeviceList)
        self.assertIsInstance(self.app.encoders(), XAMusicEncoderList)
        self.assertIsInstance(self.app.eq_presets(), XAMusicEQPresetList)
        self.assertIsInstance(self.app.eq_windows(), XAMusicEQWindowList)
        self.assertIsInstance(self.app.miniplayer_windows(), XAMusicMiniplayerWindowList)
        self.assertIsInstance(self.app.sources(), XAMusicSourceList)
        self.assertIsInstance(self.app.tracks(), XAMusicTrackList)
        self.assertIsInstance(self.app.visuals(), XAMusicVisualList)

        self.assertIsInstance(self.app.airplay_devices().xa_elem, ScriptingBridge.SBElementArray)
        self.assertIsInstance(self.app.encoders().xa_elem, ScriptingBridge.SBElementArray)
        self.assertIsInstance(self.app.eq_presets().xa_elem, ScriptingBridge.SBElementArray)
        self.assertIsInstance(self.app.eq_windows().xa_elem, ScriptingBridge.SBElementArray)
        self.assertIsInstance(self.app.miniplayer_windows().xa_elem, ScriptingBridge.SBElementArray)
        self.assertIsInstance(self.app.sources().xa_elem, ScriptingBridge.SBElementArray)
        self.assertIsInstance(self.app.tracks().xa_elem, ScriptingBridge.SBElementArray)
        self.assertIsInstance(self.app.visuals().xa_elem, ScriptingBridge.SBElementArray)

        self.assertIsInstance(self.app.airplay_devices()[0], XAMusicAirPlayDevice)
        self.assertIsInstance(self.app.encoders()[0], XAMusicEncoder)
        self.assertIsInstance(self.app.eq_presets()[0], XAMusicEQPreset)
        self.assertIsInstance(self.app.sources()[0], XAMusicSource)
        self.assertIsInstance(self.app.tracks()[0], XAMusicTrack)
        self.assertIsInstance(self.app.visuals()[0], XAMusicVisual)

        self.assertIsInstance(self.app.airplay_devices()[0].xa_elem, ScriptingBridge.SBObject)
        self.assertIsInstance(self.app.encoders()[0].xa_elem, ScriptingBridge.SBObject)
        self.assertIsInstance(self.app.eq_presets()[0].xa_elem, ScriptingBridge.SBObject)
        self.assertIsInstance(self.app.sources()[0].xa_elem, ScriptingBridge.SBObject)
        self.assertIsInstance(self.app.tracks()[0].xa_elem, ScriptingBridge.SBObject)
        self.assertIsInstance(self.app.visuals()[0].xa_elem, ScriptingBridge.SBObject)

        self.assertIsInstance(self.app.audio_cd_playlists(), XAMusicAudioCDPlaylistList)
        self.assertIsInstance(self.app.radio_tuner_playlists(), XAMusicRadioTunerPlaylistList)
        self.assertIsInstance(self.app.subscription_playlists(), XAMusicSubscriptionPlaylistList)

    def test_music_application_methods(self):
        # Test all stop
        self.app.stop()
        self.assertEqual(self.app.player_state, self.app.PlayerState.STOPPED)

        # Test playlist playback #1
        playlist = self.app.playlists().by_name("test")
        playlist.play()
        self.assertEqual(self.app.player_state, self.app.PlayerState.PLAYING)
        self.assertTrue(self.app.current_track.name in playlist.tracks().name())
        self.app.playpause()

        self.assertEqual(self.app.player_state, self.app.PlayerState.STOPPED)

        # Test playlist playback #2
        self.app.play(playlist)
        self.assertTrue(self.app.current_track.name in playlist.tracks().name())
        self.app.stop()

        # Test track playback #1
        track = self.app.tracks()[0]
        track.play()
        self.assertEqual(self.app.current_track.name, track.name)
        self.app.stop()

        # Test track playback #1
        self.app.play(track)
        self.assertEqual(self.app.current_track.name, track.name)
        self.app.stop()

    def test_music_airplay_devices(self):
        devices = self.app.airplay_devices()

        self.assertIsInstance(devices.active(), list)
        self.assertIsInstance(devices.active()[0], bool)
        self.assertIsInstance(devices.by_active(devices.active()[0]), XAMusicAirPlayDevice)

        self.assertIsInstance(devices.available(), list)
        self.assertIsInstance(devices.available()[0], bool)
        self.assertIsInstance(devices.by_available(devices.available()[0]), XAMusicAirPlayDevice)

        self.assertIsInstance(devices.kind(), list)
        self.assertIsInstance(devices.kind()[0], XAMusicApplication.DeviceKind)
        self.assertIsInstance(devices.by_kind(devices.kind()[0]), XAMusicAirPlayDevice)

        self.assertIsInstance(devices.protected(), list)
        self.assertIsInstance(devices.protected()[0], bool)
        self.assertIsInstance(devices.by_protected(devices.protected()[0]), XAMusicAirPlayDevice)

        self.assertIsInstance(devices.selected(), list)
        self.assertIsInstance(devices.selected()[0], bool)
        self.assertIsInstance(devices.by_selected(devices.selected()[0]), XAMusicAirPlayDevice)

        self.assertIsInstance(devices.supports_audio(), list)
        self.assertIsInstance(devices.supports_audio()[0], bool)
        self.assertIsInstance(devices.by_supports_audio(devices.supports_audio()[0]), XAMusicAirPlayDevice)

        self.assertIsInstance(devices.supports_video(), list)
        self.assertIsInstance(devices.supports_video()[0], bool)
        self.assertIsInstance(devices.by_supports_video(devices.supports_video()[0]), XAMusicAirPlayDevice)

        self.assertIsInstance(devices.sound_volume(), list)
        self.assertIsInstance(devices.sound_volume()[0], int)
        self.assertIsInstance(devices.by_sound_volume(devices.sound_volume()[0]), XAMusicAirPlayDevice)

        device = devices[0]
        self.assertIsInstance(device.active, bool)
        self.assertIsInstance(device.available, bool)
        self.assertIsInstance(device.kind, XAMusicApplication.DeviceKind)
        self.assertIsInstance(device.protected, bool)
        self.assertIsInstance(device.selected, bool)
        self.assertIsInstance(device.supports_audio, bool)
        self.assertIsInstance(device.supports_video, bool)
        self.assertIsInstance(device.sound_volume, int)

    def test_music_encoders(self):
        encoders = self.app.encoders()

        self.assertIsInstance(encoders.format(), list)
        self.assertIsInstance(encoders.format()[0], str)
        self.assertIsInstance(encoders.by_format(encoders.format()[0]), XAMusicEncoder)

        encoder = encoders[0]
        self.assertIsInstance(encoder.format, str)

    def test_music_eq_presets(self):
        eq_presets = self.app.eq_presets()

        self.assertIsInstance(eq_presets.band1(), list)
        self.assertIsInstance(eq_presets.band1()[0], float)
        self.assertIsInstance(eq_presets.by_band1(eq_presets.band1()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.band2(), list)
        self.assertIsInstance(eq_presets.band2()[0], float)
        self.assertIsInstance(eq_presets.by_band2(eq_presets.band2()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.band3(), list)
        self.assertIsInstance(eq_presets.band3()[0], float)
        self.assertIsInstance(eq_presets.by_band3(eq_presets.band3()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.band4(), list)
        self.assertIsInstance(eq_presets.band4()[0], float)
        self.assertIsInstance(eq_presets.by_band4(eq_presets.band4()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.band5(), list)
        self.assertIsInstance(eq_presets.band5()[0], float)
        self.assertIsInstance(eq_presets.by_band5(eq_presets.band5()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.band6(), list)
        self.assertIsInstance(eq_presets.band6()[0], float)
        self.assertIsInstance(eq_presets.by_band6(eq_presets.band6()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.band7(), list)
        self.assertIsInstance(eq_presets.band7()[0], float)
        self.assertIsInstance(eq_presets.by_band7(eq_presets.band7()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.band8(), list)
        self.assertIsInstance(eq_presets.band8()[0], float)
        self.assertIsInstance(eq_presets.by_band8(eq_presets.band8()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.band9(), list)
        self.assertIsInstance(eq_presets.band9()[0], float)
        self.assertIsInstance(eq_presets.by_band9(eq_presets.band9()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.band10(), list)
        self.assertIsInstance(eq_presets.band10()[0], float)
        self.assertIsInstance(eq_presets.by_band10(eq_presets.band10()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.modifiable(), list)
        self.assertIsInstance(eq_presets.modifiable()[0], bool)
        self.assertIsInstance(eq_presets.by_modifiable(eq_presets.modifiable()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.preamp(), list)
        self.assertIsInstance(eq_presets.preamp()[0], float)
        self.assertIsInstance(eq_presets.by_preamp(eq_presets.preamp()[0]), XAMusicEQPreset)

        self.assertIsInstance(eq_presets.update_tracks(), list)
        self.assertIsInstance(eq_presets.update_tracks()[0], bool)
        self.assertIsInstance(eq_presets.by_update_tracks(eq_presets.update_tracks()[0]), XAMusicEQPreset)

        eq_preset = eq_presets[0]
        self.assertIsInstance(eq_preset.band1, float)
        self.assertIsInstance(eq_preset.band2, float)
        self.assertIsInstance(eq_preset.band3, float)
        self.assertIsInstance(eq_preset.band4, float)
        self.assertIsInstance(eq_preset.band5, float)
        self.assertIsInstance(eq_preset.band6, float)
        self.assertIsInstance(eq_preset.band7, float)
        self.assertIsInstance(eq_preset.band8, float)
        self.assertIsInstance(eq_preset.band9, float)
        self.assertIsInstance(eq_preset.band10, float)
        self.assertIsInstance(eq_preset.modifiable, bool)
        self.assertIsInstance(eq_preset.preamp, float)
        self.assertIsInstance(eq_preset.update_tracks, bool)
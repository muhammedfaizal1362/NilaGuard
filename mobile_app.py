from kivy.app import App
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.utils import get_color_from_hex
import random

from src.analyzer import analyze_message
from src.url_analyzer import analyze_url

BG = '#07111F'
PANEL = '#101D2E'
PANEL2 = '#14243A'
CYAN = '#38D9F5'
BLUE = '#397BFF'
WHITE = '#EAF3FF'
MUTED = '#91A6BD'
GREEN = '#43D69A'
AMBER = '#FFBD59'
RED = '#FF657A'


def rgba(hex_color):
    return get_color_from_hex(hex_color)


class Card(BoxLayout):
    def __init__(self, color=PANEL, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*rgba(color))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
        self.bind(pos=self._sync, size=self._sync)
        self.opacity = 0
        Animation(opacity=1, duration=.35).start(self)

    def _sync(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size


class NGLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('color', rgba(WHITE))
        kwargs.setdefault('font_size', '14sp')
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'middle')
        super().__init__(**kwargs)
        self.bind(size=self._text_size)

    def _text_size(self, *_):
        self.text_size = self.size


class NGButton(Button):
    def __init__(self, bg=CYAN, fg=BG, **kwargs):
        kwargs.setdefault('background_normal', '')
        kwargs.setdefault('background_down', '')
        kwargs.setdefault('background_color', rgba(bg))
        kwargs.setdefault('color', rgba(fg))
        kwargs.setdefault('font_size', '14sp')
        kwargs.setdefault('bold', True)
        super().__init__(**kwargs)
        self.bind(on_press=self._button_press, on_release=self._button_release)

    def _button_press(self, *_):
        Animation(opacity=0.72, duration=0.08).start(self)

    def _button_release(self, *_):
        Animation(opacity=1, duration=0.16).start(self)


class NilaGuardApp(App):
    def build(self):
        self.title = 'NilaGuard'
        self.mode = 'message'
        self.page = 'home'
        self.history = []
        self.scan_busy = False
        self.scan_progress = 0
        self.cyan = rgba(CYAN)
        self.muted = rgba(MUTED)
        root = BoxLayout(orientation='vertical', padding=[dp(14), dp(12), dp(14), dp(10)], spacing=dp(10))
        with root.canvas.before:
            Color(*rgba(BG))
            self.bg_rect = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._root_bg, size=self._root_bg)
        self.root_box = root
        self._particles = []
        self._particle_event = None
        with root.canvas.before:
            Color(0.10, 0.35, 0.55, 0.12)
            self._circuit_lines = [
                Line(points=[0, 0, 0, 0], width=1),
                Line(points=[0, 0, 0, 0], width=1),
                Line(points=[0, 0, 0, 0], width=1),
            ]
        self._create_particles(root)
        self.body = BoxLayout(orientation='vertical', spacing=dp(10))
        root.add_widget(self.body)
        self.nav = self.make_nav()
        root.add_widget(self.nav)
        self.show_page('welcome')
        return root

    def _create_particles(self, root):
        with root.canvas.before:
            for _ in range(8):
                x = random.uniform(0, root.width or 400)
                y = random.uniform(0, root.height or 800)
                speed = random.uniform(8, 22)
                size = random.uniform(1.5, 3.5)
                Color(0.20, 0.75, 1.0, random.uniform(0.12, 0.38))
                dot = Ellipse(pos=(x, y), size=(size, size))
                self._particles.append([dot, x, y, speed, size])
        self._particle_event = Clock.schedule_interval(self._animate_background, 1/8)

    def _animate_background(self, dt):
        if not hasattr(self, '_particles'):
            return
        height = self.root_box.height
        width = self.root_box.width
        for item in self._particles:
            dot, x, y, speed, size = item
            y += speed * dt
            if y > height + 10:
                y = -10
                x = random.uniform(0, width)
            item[1], item[2] = x, y
            dot.pos = (x, y)
    def _root_bg(self, *_):
        self.bg_rect.pos = self.root_box.pos
        self.bg_rect.size = self.root_box.size

    def make_header(self):
        h = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), spacing=dp(10))
        h.padding = [0, dp(15), 0, 0]
        logo = NGLabel(text='N', font_size='36sp', color=self.cyan, size_hint_x=None, width=dp(52))
        titles = BoxLayout(orientation='vertical', spacing=0)
        titles.add_widget(NGLabel(text='[b]NilaGuard[/b]', markup=True, font_size='25sp', color=self.cyan))
        titles.add_widget(NGLabel(text='MULTILINGUAL SCAM DEFENSE', font_size='10sp', color=self.muted))
        h.add_widget(logo)
        h.add_widget(titles)
        return h

    def make_nav(self):
        nav = Card(orientation='horizontal', size_hint_y=None, height=dp(58),
                   padding=[dp(5), dp(5)], spacing=dp(4), color=PANEL)
        for name, label in [('home', '⌂  Home'), ('scan', '⌕  Scan'),
                            ('history', '◷  History'), ('about', 'ⓘ  About')]:
            b = NGButton(text=label, bg=PANEL2, fg=WHITE, font_size='12sp')
            b.bind(on_press=lambda _, p=name: self.show_page(p))
            nav.add_widget(b)
        return nav

    def clear_body(self):
        self.body.clear_widgets()

    def show_page(self, page):
        if self.scan_busy and page not in ('scan', 'result'):
            return
        self.page = page
        self.clear_body()
        if page == 'welcome':
            self.welcome_page()
            self.nav.opacity = 0
            self.nav.height = 0
        else:
            self.nav.opacity = 1
            self.nav.height = dp(58)
        if page == 'welcome':
            pass
        elif page == 'home':
            self.home_page()
        elif page == 'scan':
            self.scan_page()
        elif page == 'history':
            self.history_page()
        elif page == 'result':
            self.result_page()
        else:
            self.about_page()
        for w in self.body.children:
            w.opacity = 0
            Animation(opacity=0.15, duration=0.01).start(w)
            Animation(opacity=0.2, duration=0.01).start(w)
            Animation(opacity=1, duration=.40).start(w)

    def welcome_page(self):
        panel = BoxLayout(orientation='vertical', spacing=dp(16), padding=[dp(22), dp(24)],
                         size_hint_y=1)
        # Subtle animated brand glow, built with ordinary Kivy widgets for portability.
        top = BoxLayout(orientation='vertical', spacing=dp(6), size_hint_y=None, height=dp(80))
        top.add_widget(NGLabel(text='NILAGUARD', font_size='12sp', color=self.cyan,
                              halign='center', bold=True))
        top.add_widget(NGLabel(text='DIGITAL SAFETY  /  SCAM AWARENESS', font_size='10sp',
                              color=self.muted, halign='center'))
        panel.add_widget(top)

        panel.add_widget(Label(text='', size_hint_y=0.12))
        shield = NGLabel(text='N', font_size='100sp', color=self.cyan, halign='center',
                         size_hint_y=None, height=dp(150))
        panel.add_widget(shield)
        pulse = Animation(font_size=dp(112), duration=0.85) + Animation(font_size=dp(96), duration=0.85)
        pulse.repeat = True
        pulse.start(shield)

        brand = NGLabel(text='[b]NilaGuard[/b]', markup=True, font_size='34sp',
                        color=self.cyan, halign='center', size_hint_y=None, height=dp(55))
        brand.opacity = 0
        panel.add_widget(brand)
        Animation(opacity=1, duration=1.0).start(brand)
        tagline = NGLabel(text='Your multilingual\nscam-defense companion', color=WHITE,
                         font_size='18sp', halign='center', size_hint_y=None, height=dp(70))
        panel.add_widget(tagline)
        panel.add_widget(Label(text='', size_hint_y=0.16))
        start = NGButton(text='GET STARTED   ›', bg=CYAN, fg=BG, font_size='18sp',
                         size_hint_y=None, height=dp(58))
        start.bind(on_press=lambda *_: self.show_page('home'))
        panel.add_widget(start)
        note = NGLabel(text='MESSAGE INTELLIGENCE  •  URL INSPECTION  •  SAFETY',
                       color=self.muted, font_size='11sp', halign='center',
                       size_hint_y=None, height=dp(36))
        panel.add_widget(note)
        self.body.add_widget(panel)

    def home_page(self):
        self.body.add_widget(self.make_header())
        scroll = ScrollView(do_scroll_x=False)
        content = BoxLayout(orientation='vertical', spacing=dp(12), padding=[0, dp(4)],
                           size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        hero = Card(orientation='vertical', padding=dp(18), spacing=dp(10),
                    size_hint_y=None, height=dp(235), color=PANEL)
        hero.add_widget(NGLabel(text='[b]DIGITAL DEFENSE CENTER[/b]',
                               markup=True, font_size='20sp', color=WHITE,
                               size_hint_y=None, height=dp(40)))
        shield = NGLabel(text='N', font_size='72sp', color=self.cyan,
                         size_hint_y=None, height=dp(90))
        hero.add_widget(shield)
        Animation(font_size=dp(78), duration=.8).start(shield)
        Animation(font_size=dp(68), duration=.8).start(shield)
        hero.add_widget(NGLabel(text='MONITOR suspicious messages and links\nusing explainable security indicators.',
                               color=self.muted, halign='center'))
        content.add_widget(hero)
        quick = Card(orientation='vertical', padding=dp(14), spacing=dp(10),
                     size_hint_y=None, height=dp(165), color=PANEL)
        quick.add_widget(NGLabel(text='[b]QUICK ACTION[/b]', markup=True, color=self.cyan,
                                size_hint_y=None, height=dp(30)))
        for label, mode in [('Message scan', 'message'), ('URL scan', 'url')]:
            btn = NGButton(text='  ' + label + '   ›', bg=PANEL2, fg=WHITE,
                           size_hint_y=None, height=dp(48), halign='left')
            btn.bind(on_press=lambda _, m=mode: self.open_scan(m))
            quick.add_widget(btn)
        content.add_widget(quick)
        info = Card(orientation='vertical', padding=dp(14), size_hint_y=None,
                    height=dp(110), color=PANEL)
        info.add_widget(NGLabel(text='[b]ANALYSIS APPROACH[/b]', markup=True,
                               color=self.cyan, size_hint_y=None, height=dp(30)))
        info.add_widget(NGLabel(text='NilaGuard checks predefined patterns and structural clues. '
                                    'It does not guarantee a message or link is safe.',
                               color=self.muted))
        content.add_widget(info)
        scroll.add_widget(content)
        self.body.add_widget(scroll)

    def open_scan(self, mode):
        self.mode = mode
        self.show_page('scan')

    def scan_page(self):
        self.body.add_widget(self.make_header())
        mode_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self.msg_btn = NGButton(text='MESSAGE SCAN', bg=CYAN if self.mode == 'message' else PANEL2,
                                fg=BG if self.mode == 'message' else WHITE)
        self.url_btn = NGButton(text='URL SCAN', bg=CYAN if self.mode == 'url' else PANEL2,
                                fg=BG if self.mode == 'url' else WHITE)
        self.msg_btn.bind(on_press=lambda _: self.set_mode('message'))
        self.url_btn.bind(on_press=lambda _: self.set_mode('url'))
        mode_row.add_widget(self.msg_btn)
        mode_row.add_widget(self.url_btn)
        self.body.add_widget(mode_row)
        self.body.add_widget(NGLabel(text='[b]INPUT[/b]', markup=True, color=self.cyan,
                                    size_hint_y=None, height=dp(28)))
        self.input_box = TextInput(
            hint_text='Paste a suspicious message here...' if self.mode == 'message' else 'Paste a URL here...',
            multiline=True, font_size='16sp', padding=[dp(12), dp(12)],
            size_hint_y=None, height=dp(145), background_normal='', background_active='',
            background_color=rgba(PANEL), foreground_color=rgba(WHITE),
            hint_text_color=rgba(MUTED), cursor_color=self.cyan)
        input_card = Card(orientation='vertical', padding=dp(8), size_hint_y=None,
                          height=dp(160), color=PANEL)
        input_card.add_widget(self.input_box)
        self.body.add_widget(input_card)
        actions = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        sample = NGButton(text='Sample', bg=PANEL2, fg=WHITE)
        sample.bind(on_press=self.load_sample)
        clear = NGButton(text='Clear', bg=PANEL2, fg=WHITE)
        clear.bind(on_press=self.clear_input)
        actions.add_widget(sample)
        actions.add_widget(clear)
        self.body.add_widget(actions)
        scan = NGButton(text='⌕   ANALYZE', bg=CYAN, fg=BG,
                        size_hint_y=None, height=dp(54), font_size='18sp')
        scan.bind(on_press=self.analyze)
        self.body.add_widget(scan)

        self.animation_card = Card(orientation='vertical', padding=dp(12), spacing=dp(8),
                                  size_hint_y=None, height=dp(110), color=PANEL)
        self.scan_visual = NGLabel(text='N', font_size='38sp', color=self.cyan,
                                  halign='center', size_hint_y=None, height=dp(50))
        self.scan_status = NGLabel(text='SYSTEM READY  •  AWAITING INPUT', color=self.muted, halign='center')
        self.progress = ProgressBar(max=100, value=0, size_hint_y=None, height=dp(12))
        self.animation_card.add_widget(self.scan_visual)
        self.animation_card.add_widget(self.scan_status)
        self.animation_card.add_widget(self.progress)
        self.body.add_widget(self.animation_card)
        self._idle_scan_anim = (
            Animation(opacity=.55, duration=.8) +
            Animation(opacity=1, duration=.8)
        )
        self._idle_scan_anim.repeat = True
        self._idle_scan_anim.start(self.scan_visual)

        self.result_card = Card(orientation='vertical', padding=dp(12), spacing=dp(8),
                                color=PANEL)
        self.result_title = NGLabel(text='[b]SCAN RESULT[/b]', markup=True, color=self.cyan,
                                    size_hint_y=None, height=dp(28))
        self.result_label = NGLabel(text='Your analysis will appear here.', color=rgba(WHITE))
        self.result_card.add_widget(self.result_title)
        self.result_card.add_widget(self.result_label)
        self.body.add_widget(self.result_card)
        self.body.add_widget(NGLabel(text='Rule-based analysis only; not a definitive security verdict.',
                                    color=self.muted, font_size='10sp', halign='center',
                                    size_hint_y=None, height=dp(28)))

    def set_mode(self, mode):
        if not self.scan_busy:
            self.mode = mode
            self.show_page('scan')

    def load_sample(self, _):
        self.input_box.text = ('Your bank account is blocked. Verify now and claim your reward.'
                               if self.mode == 'message' else 'https://example.com')
        self.result_label.text = 'Sample loaded. Press Analyze to scan.'

    def clear_input(self, _):
        if self.scan_busy:
            return
        self.input_box.text = ''
        self.result_label.text = 'Your analysis will appear here.'
        self.progress.value = 0
        self.scan_status.text = 'Ready to scan'

    def analyze(self, _):
        if self.scan_busy:
            return
        value = self.input_box.text.strip()
        if not value:
            self.result_label.text = 'Please enter input first.'
            return
        self.scan_busy = True
        Animation.cancel_all(self.scan_visual)
        self.scan_visual.opacity = 1
        self.scan_progress = 0
        self.progress.value = 0
        self.result_label.text = ''
        self.result_card.opacity = 0
        self.scan_status.text = 'INITIALIZING SECURITY SCAN...'
        self.scan_visual.text = 'N'
        self.scan_visual.font_size = dp(38)
        self._pulse = Animation(font_size=dp(46), duration=.35) + Animation(font_size=dp(38), duration=.35)
        self._pulse.repeat = True
        self._pulse.start(self.scan_visual)
        self._scan_event = Clock.schedule_interval(self._scan_tick, .06)
        self._pending_value = value

    def _scan_tick(self, dt):
        self.scan_progress += 4
        Animation(value=min(100, self.scan_progress), duration=.12).start(self.progress)
        frames = ['N', '+', '*', '+']
        self.scan_visual.text = frames[(self.scan_progress // 8) % len(frames)]
        if self.scan_progress < 35:
            self.scan_status.text = '01  /  INSPECTING INPUT...'
        elif self.scan_progress < 70:
            self.scan_status.text = '02  /  CHECKING INDICATORS...'
        else:
            self.scan_status.text = '03  /  PREPARING REPORT...'
        if self.scan_progress >= 100:
            self._scan_event.cancel()
            self._pulse.cancel(self.scan_visual)
            Clock.schedule_once(lambda _: self.perform_analysis(self._pending_value), .12)
            return False
        return True

    def perform_analysis(self, value):
        try:
            if self.mode == 'message':
                result = analyze_message(value)
                findings = '\n'.join('• {} — {}'.format(x.get('category', 'Indicator'),
                               x.get('matched_indicator', '')) for x in result.get('findings', []))
                findings = findings or 'No predefined indicators detected.'
                score = result.get('score', 0)
                level = result.get('level', 'Unknown')
                output = ('[b]MESSAGE ANALYSIS[/b]\n\n[b]Risk score:[/b] {}%\n'
                          '[b]Result:[/b] {}\n\n[b]Indicators[/b]\n{}\n\n{}\n\n'
                          '[i]Rule-based assessment only.[/i]').format(score, level, findings,
                                                                       result.get('message', ''))
                color = RED if int(score or 0) >= 70 else (AMBER if int(score or 0) >= 35 else GREEN)
            else:
                result = analyze_url(value)
                findings = '\n'.join('• {}'.format(x) for x in result.get('findings', []))
                findings = findings or 'No structural indicators detected.'
                output = ('[b]URL ANALYSIS[/b]\n\n[b]Format valid:[/b] {}\n'
                          '[b]Hostname:[/b] {}\n\n[b]Findings[/b]\n{}\n\n{}\n\n'
                          '[i]Structural analysis only. The URL was not opened.[/i]').format(
                              result.get('valid', 'N/A'), result.get('hostname', 'N/A'),
                              findings, result.get('message', ''))
                score = None
                level = 'URL review'
                color = CYAN
            self.latest_output = output
            self.latest_score = score
            self.latest_level = level
            self.latest_color = color
            self.latest_mode = self.mode
            self.history.insert(0, {'mode': self.mode, 'input': value[:100], 'output': output,
                                    'score': score, 'level': level})
            self.scan_status.text = 'SCAN COMPLETE  /  REPORT READY'
            self.scan_visual.text = '✓'
            self.scan_visual.color = rgba(color)
            Clock.schedule_once(lambda dt: self.show_page('result'), .15)
        except Exception as e:
            self.result_label.text = 'Analysis could not be completed.\n{}'.format(str(e))
            self.result_label.markup = False
            self.scan_status.text = 'Scan error'
        finally:
            self.scan_busy = False

    def result_page(self):
        self.body.add_widget(self.make_header())

        scroll = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        content = BoxLayout(orientation='vertical', spacing=dp(14),
                           padding=[dp(10), dp(12)], size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        hero = Card(orientation='vertical', padding=dp(18), spacing=dp(8),
                    size_hint_y=None, height=dp(245), color=PANEL)

        hero.add_widget(NGLabel(text='[b]// THREAT ASSESSMENT[/b]',
            markup=True, color=self.cyan, halign='center',
            size_hint_y=None, height=dp(35)))

        if self.latest_score is not None:
            score = int(self.latest_score or 0)

            if score >= 70:
                risk_text = 'HIGH RISK'
                risk_color = RED
            elif score >= 35:
                risk_text = 'MEDIUM RISK'
                risk_color = AMBER
            else:
                risk_text = 'LOW RISK'
                risk_color = GREEN

            score_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None, height=dp(95),
                spacing=dp(12)
            )

            score_row.add_widget(NGLabel(
                text=str(score) + '%',
                font_size='58sp', bold=True,
                color=rgba(self.latest_color),
                halign='right'
            ))

            score_row.add_widget(NGLabel(
                text='[b]{}[/b]'.format(risk_text),
                markup=True, font_size='17sp',
                color=rgba(risk_color),
                halign='left'
            ))

            hero.add_widget(score_row)

        else:
            hero.add_widget(NGLabel(
                text='URL // REVIEW',
                font_size='30sp', color=self.cyan,
                halign='center',
                size_hint_y=None, height=dp(100)
            ))

        hero.add_widget(NGLabel(
            text='[color=43D69A]●[/color]  ANALYSIS COMPLETE',
            markup=True, color=self.muted, halign='center'
        ))
        content.add_widget(hero)

        detail = Card(orientation='vertical', padding=dp(16),
            spacing=dp(12), size_hint_y=None,
            height=dp(470), color=PANEL2)

        detail.add_widget(NGLabel(
            text='[b]// FINDINGS & REPORT[/b]',
            markup=True, color=self.cyan,
            size_hint_y=None, height=dp(38)
        ))

        formatted = self.latest_output.replace('\n', '\n\n')
        report = NGLabel(text=formatted, markup=True,
            color=rgba(WHITE), halign='left', valign='top',
            size_hint=(1, None), height=dp(390))
        report.bind(width=lambda w, width: setattr(
            w, 'text_size', (width, dp(390))))
        detail.add_widget(report)
        content.add_widget(detail)

        note = Card(orientation='vertical', padding=dp(14),
            size_hint_y=None, height=dp(90), color=PANEL)
        note.add_widget(NGLabel(
            text='[b]NOTE[/b]\nAutomated indicators are not a definitive verdict. Verify independently.',
            markup=True, color=self.muted, halign='center'
        ))
        content.add_widget(note)

        again = NGButton(text='[ SCAN AGAIN ]', bg=CYAN, fg=BG,
            size_hint_y=None, height=dp(54))
        again.bind(on_press=lambda *_: self.open_scan(self.latest_mode))
        content.add_widget(again)

        home = NGButton(text='[ RETURN TO DASHBOARD ]', bg=PANEL,
            fg=WHITE, size_hint_y=None, height=dp(50))
        home.bind(on_press=lambda *_: self.show_page('home'))
        content.add_widget(home)

        scroll.add_widget(content)
        self.body.add_widget(scroll)

    def history_page(self):
        self.body.add_widget(self.make_header())
        self.body.add_widget(NGLabel(text='[b]SCAN HISTORY[/b]', markup=True, color=self.cyan,
                                    size_hint_y=None, height=dp(32)))
        scroll = ScrollView(do_scroll_x=False)
        items = BoxLayout(orientation='vertical', spacing=dp(10), padding=[0, dp(5)],
                         size_hint_y=None)
        items.bind(minimum_height=items.setter('height'))
        if not self.history:
            empty = Card(orientation='vertical', padding=dp(18), size_hint_y=None,
                         height=dp(120), color=PANEL)
            empty.add_widget(NGLabel(text='No scans in this session yet.\nYour recent scan summaries will appear here.',
                                    color=self.muted, halign='center'))
            items.add_widget(empty)
        else:
            for item in self.history:
                c = Card(orientation='vertical', padding=dp(12), spacing=dp(5),
                         size_hint_y=None, height=dp(105), color=PANEL)
                c.add_widget(NGLabel(text='[b]{}[/b]   {}'.format(item['mode'].upper(),
                               item.get('level', '')), markup=True, color=self.cyan,
                               size_hint_y=None, height=dp(28)))
                c.add_widget(NGLabel(text=item['input'], color=rgba(WHITE)))
                items.add_widget(c)
        scroll.add_widget(items)
        self.body.add_widget(scroll)
        clear = NGButton(text='Clear session history', bg=PANEL2, fg=WHITE,
                         size_hint_y=None, height=dp(45))
        clear.bind(on_press=lambda _: self.clear_history())
        self.body.add_widget(clear)

    def clear_history(self):
        self.history.clear()
        self.show_page('history')

    def about_page(self):
        self.body.add_widget(self.make_header())
        scroll = ScrollView(do_scroll_x=False)
        c = Card(orientation='vertical', padding=dp(18), spacing=dp(12),
                 size_hint_y=None, height=dp(510), color=PANEL)
        c.add_widget(NGLabel(text='[b]NILAGUARD  /  SYSTEM INFO[/b]', markup=True, color=self.cyan,
                            size_hint_y=None, height=dp(35)))
        c.add_widget(NGLabel(text='NilaGuard is a multilingual scam-awareness assistant designed to highlight predefined indicators in suspicious messages and URLs.',
                            color=rgba(WHITE)))
        c.add_widget(NGLabel(text='[b]Privacy & limitations[/b]', markup=True, color=CYAN,
                            size_hint_y=None, height=dp(30)))
        c.add_widget(NGLabel(text='• Analysis is rule-based and may miss or misclassify content.\n\n'
                            '• No URL is opened during structural analysis.\n\n'
                            '• Do not treat a result as proof that content is safe or malicious.\n\n'
                            '• Avoid entering sensitive personal information.',
                            color=rgba(MUTED)))
        c.add_widget(NGLabel(text='[b]Version[/b]   Prototype 0.2', markup=True, color=rgba(WHITE),
                            size_hint_y=None, height=dp(30)))
        c.add_widget(NGLabel(text='[b]DEVELOPED BY[/b]\nMuhammed Faizal\nCybersecurity Enthusiast | Student Developer',
                            markup=True, color=self.cyan, halign='center',
                            size_hint_y=None, height=dp(95)))
        scroll.add_widget(c)
        self.body.add_widget(scroll)


if __name__ == '__main__':
    NilaGuardApp().run()


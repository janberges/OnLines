#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from scipy import log, linspace, sin, pi
from random import random
from re import sub
import os
from subprocess import call

def ceil(n = 0.0, f = 1.0):
    return f * (n // f + (n / f > n // f))

def round(n = 0.0, f = 1.0):
    return f * int(n / f + 0.5 * cmp(n, 0))

def floor(n = 0.0, f = 1.0):
    return f * (n // f - (n / f < n // f))

def lg(x):
    return log(x) / log(10.0)

def order(x):
    return 10.0 ** floor(lg(abs(x))) if x else 1.0

def round_mantissa(n = 0.0, f = 1.0):
    return round(n, f * order(n))

def multiples(min = 0.0, max = 0.0, f = 1.0):
    return [_ * f for _ in range(int(ceil(min / f)), int(floor(max / f) + 1))]

def plot(
    name = 'untitled',
    save = False,

    x_label = 'x',
    y_label = 'y',
    legend = None,

    background_image = None,

    font_family = 'Sans, sans-serif',
    font_size = 9.0,
    line_height = 1.4,
    baseline_shift = 1.0 / 3,

    width = 700.0,
    height = 500.0,

    margin = None,
    margin_left = None,
    margin_right = None,
    margin_bottom = None,
    margin_top = None,

    legend_left = None,
    legend_top = None,

    x_ref = None,
    y_ref = None,
    x_min = None,
    x_max = None,
    y_min = None,
    y_max = None,

    x_tick_spacing = 80.0,
    y_tick_spacing = 80.0,
    x_tick_interval = None,
    y_tick_interval = None,
    x_ticks = None,
    y_ticks = None,

    marker_size = 6.0,

    defs = '',
    before = '',
    after = '',

    axes = True,

    fill = 'none',
    stroke = 'black',
    stroke_width = 0.5,

    plots = []):

    standard = dict(
        x = [0],
        y = [0],
        dx = [0],
        dy = [0],
        txt = [''],
        )

    for plot in plots:
        n = 1

        for key in standard:
            if key not in plot:
                plot[key] = standard[key]

            try:
                plot[key][0]
            except:
                plot[key] = [plot[key]]

            if len(plot[key]) > n:
                n = len(plot[key])

        for key in standard:
            plot[key] = [plot[key][_ % len(plot[key])] for _ in range(n)]

    if x_min is None:
        x_min = min(x - abs(dx) for _ in plots for x, dx in zip(_['x'], _['dx']))

    if x_max is None:
        x_max = max(x + abs(dx) for _ in plots for x, dx in zip(_['x'], _['dx']))

    if y_min is None:
        y_min = min(y - abs(dy) for _ in plots for y, dy in zip(_['y'], _['dy']))

    if y_max is None:
        y_max = max(y + abs(dy) for _ in plots for y, dy in zip(_['y'], _['dy']))

    if x_ref is not None:
        x_min = min(x_min, x_ref)
        x_max = max(x_max, x_ref)

    if y_ref is not None:
        y_min = min(y_min, y_ref)
        y_max = max(y_max, y_ref)

    dx = x_max - x_min or 1.0
    dy = y_max - y_min or 1.0

    defs += "<path id='wave' d='M -{0} 0 C 0 -{font_size} 0 {font_size} {0} 0' /><marker id='arrow' viewBox='-{marker_size} -{marker_size} {1} {1}' markerWidth='{1}' markerHeight='{1}' orient='auto'><path fill='{fill}' stroke='{stroke}' stroke_width='1' d='M -{marker_size} -{marker_size} l {marker_size} {marker_size} l -{marker_size} {marker_size}' /></marker>".format(0.5 * font_size, 2.0 * marker_size, **vars())

    baseline_shift *= font_size
    line_height *= font_size
    marker_size *= stroke_width

    x_label_spacing = marker_size
    if x_ticks != []:
        x_label_spacing += line_height

    y_label_spacing = marker_size
    if y_ticks != []:
        y_label_spacing += line_height

    if margin is not None:
        margin_left = margin
        margin_top = margin
        margin_right = margin
        margin_bottom = margin
    else:
        if margin_left is None:
            margin_left = y_label_spacing + line_height

        if margin_top is None:
            margin_top = 3 * marker_size

        if margin_right is None:
            margin_right = 3 * marker_size

        if margin_bottom is None:
            margin_bottom = x_label_spacing + line_height

    if width:
        inner_width = width - margin_left - margin_right
        h_per_x = inner_width / dx

    if height:
        inner_height = height - margin_bottom - margin_top
        v_per_y = -inner_height / dy

    if not width:
        inner_width = inner_height * dx / dy
        width = inner_width + margin_left + margin_right
        h_per_x = -v_per_y

    if not height:
        inner_height = inner_width * dy / dx
        height = inner_height + margin_bottom + margin_top
        v_per_y = -h_per_x

    left = margin_left
    right = width - margin_right
    bottom = height - margin_bottom
    top = margin_top

    if legend_left is None:
        legend_left = left + line_height

    if legend_top is None:
        legend_top = top

    legend_top += 0.5 * line_height

    x_to_h = lambda x: h_per_x * (x - x_min) + left
    y_to_v = lambda y: v_per_y * (y - y_min) + bottom

    def format(x):
        x = sub(r'<(.+?)>\{', r"<tspan fill='\1'>", x)
        x = x.replace('[', "<tspan style='font-style: italic'>")
        x = x.replace('^{', "<tspan baseline-shift='super' style='font-size: {}px'>".format(0.75 * font_size))
        x = x.replace('_{', "<tspan baseline-shift='sub' dominant-baseline='mathematical' style='font-size: {}px'>".format(0.75 * font_size))
        x = x.replace('{', "<tspan style='font-weight: bold'>".format(+baseline_shift, 0.75 * font_size))
        x = sub(r'\}|\]', r"</tspan>", x)
        x = x.replace('--', '&#8722;')
        x = x.replace('_', '&#8201;')
        return x

    text = "style='font-family: {font_family}; font-size: {font_size}px; line-height: {line_height}px' dy='{baseline_shift}'".format(**vars())

    svg = "<svg id='{name}' width='{width}' height='{height}' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' version='1.1'><defs>".format(**vars())

    svg += defs.format(**vars())

    svg += "</defs>"

    svg += before.format(**vars())

    if background_image:
        svg += "<image x='{left}' y='{top}' width='{inner_width}' height='{inner_height}' xlink:href='{background_image}' />".format(**vars())

    h_ref = x_to_h(x_ref) if x_ref is not None else left
    v_ref = y_to_v(y_ref) if y_ref is not None else bottom

    if abs(h_ref - left) > 1:
        svg += "<path d='M {h_ref} {bottom} L {h_ref} {top}' stroke='#888' stroke-width='{stroke_width}' stroke-dasharray='3 3' />".format(**vars())

    if abs(v_ref - bottom) > 1:
        svg += "<path d='M {left} {v_ref} L {right} {v_ref}' stroke='#888' stroke-width='{stroke_width}' stroke-dasharray='3 3' />".format(**vars())

    if legend is not None:
        legend = format(legend)
        svg += "<text {text} x='{legend_left}' y='{legend_top}' text-anchor='start'>{legend}</text>".format(**vars())
        legend_top += line_height

    colors = ['blue', 'green', 'red', 'orange', 'turquoise', 'purple', 'black', 'grey']

    for plot in plots:
        attributes = dict(
            line = dict(
                fill = 'none',
                stroke = colors[0],
                stroke_width = stroke_width,
                ),
            circle = dict(
                fill = colors[0],
                stroke_width = stroke_width,
                r = 0.5 * marker_size,
                ),
            ellipse = dict(
                fill = 'none',
                stroke = stroke,
                stroke_width = stroke_width,
                stroke_dasharray = '3 2',
                ),
            bar = dict(
                fill = colors[0],
                stroke = stroke,
                stroke_width = stroke_width,
                ),
            cross = dict(
                stroke = colors[0],
                stroke_width = stroke_width,
                ),
            text = dict(
                font_family = font_family,
                font_size = font_size,
                line_height = line_height,
                text_anchor = 'middle',
                ),
            quadratic = dict(
                fill = 'none',
                stroke = colors[0],
                stroke_width = stroke_width,
                ),
            smooth = dict(
                fill = 'none',
                stroke = colors[0],
                stroke_width = stroke_width,
                )
            )

        colors = colors[1:] + colors[:1]

        for key in plot:
            if key in attributes:
			    attributes[key].update(plot[key])

        for key, value in attributes.items():
            attributes[key] = ' '.join('''{}="{}"'''.format(k.replace('_', '-').lower(), v) for k, v in value.items())

        H   = [x_to_h(x)     for x   in plot['x'  ]]
        V   = [y_to_v(y)     for y   in plot['y'  ]]
        DH  = [h_per_x * dx  for dx  in plot['dx' ]]
        DV  = [-v_per_y * dy for dy  in plot['dy' ]]
        TXT = [format(txt)   for txt in plot['txt']]

        if 'line' in plot:
            if x_ref is not None:
                H1 = [h_ref] + H + [h_ref]
                V1 = V[:1] + V + V[-1:]
            elif y_ref is not None:
                H1 = H[:1] + H + H[-1:]
                V1 = [v_ref] + V + [v_ref]
            else:
                H1 = H
                V1 = V

            svg += "<polyline points='{0}' {attributes[line]} />".format(' '.join(str(_) for _ in zip(H1, V1) for _ in _), **vars())

        if 'quadratic' in plot:
            svg += "<path d='M {H[0]} {V[0]} Q {0}' {attributes[quadratic]} />".format(' '.join(str(_) for _ in zip(H[1:], V[1:]) for _ in _), **vars())

        if 'smooth' in plot:
            svg += "<path d='M {H[0]} {V[0]} S {0}' {attributes[smooth]} />".format(' '.join(str(_) for _ in zip(H[1:], V[1:]) for _ in _), **vars())

        if 'legend' in plot:
            H.append(legend_left + 0.5 * font_size)
            V.append(legend_top)
            DH.append(0.5 * font_size)
            DV.append(0.5 * font_size)
            TXT.append('abc')

            plot['legend'] = format(plot['legend'])

            svg += "<text {text} x='{legend_left}' y='{legend_top}' dx='{line_height}' text-anchor='start'>{plot[legend]}</text>".format(**vars())

            if 'line' in plot:
                svg += "<use xlink:href='#wave' x='{0}' y='{1}' {attributes[line]} />".format(H[-1], V[-1], **vars())

            if 'quadratic' in plot:
                svg += "<use xlink:href='#wave' x='{0}' y='{1}' {attributes[line]} />".format(H[-1], V[-1], **vars())

            legend_top += line_height

        if 'circle' in plot:
            for h, v in zip(H, V):
                svg += "<circle cx='{h}' cy='{v}' {attributes[circle]} />".format(**vars())

        if 'ellipse' in plot:
            for h, v, dh, dv in zip(H, V, DH, DV):
                svg += "<ellipse cx='{h}' cy='{v}' rx='{dh}' ry='{dv}' {attributes[ellipse]} />".format(**vars())

        if 'bar' in plot:
            for h, v, dh, dv in zip(H, V, DH, DV):
                svg += "<path d='M {0} {1} h {2} v {3} h {4} Z' {attributes[bar]} />".format(h + dh, v + dv, -2 * dh or h_ref - h, -2 * dv or v_ref - v, 2 * dh or h - h_ref, **vars())

        if 'cross' in plot:
            svg += "<g {attributes[cross]}>".format(**vars())

            for h, v, dh, dv in zip(H, V, DH, DV):
                if dh:
                    svg += "<path d='M {0} {v} L {1} {v}' /><path d='M {0} {2} v {marker_size}' /><path d='M {1} {2} v {marker_size}' />".format(h - dh, h + dh, v - 0.5 * marker_size, **vars())
                if dv:
                    svg += "<path d='M {h} {0} L {h} {1}' /><path d='M {2} {0} h {marker_size}' /><path d='M {2} {1} h {marker_size}' />".format(v - dv, v + dv, h - 0.5 * marker_size, **vars())

            svg += "</g>"

        if 'text' in plot:
            for h, v, txt in zip(H, V, TXT):
                svg += "<g transform='translate({h}, {v})'><text {attributes[text]}>{txt}</text></g>".format(**vars())

    if axes:
        if x_ticks is None:
            if x_tick_interval is None:
                x_tick_interval = abs(round_mantissa(x_tick_spacing / h_per_x))
            x_ticks = multiples(x_min, x_max, x_tick_interval)

        if y_ticks is None:
            if y_tick_interval is None:
                y_tick_interval = abs(round_mantissa(y_tick_spacing / v_per_y))
            y_ticks = multiples(y_min, y_max, y_tick_interval)

        nice = lambda x: '{0:g}'.format(x).replace('-', '&#8722;')

        if type(x_ticks) is not dict:
            x_ticks = dict(zip(x_ticks, map(nice, x_ticks)))

        if type(y_ticks) is not dict:
            y_ticks = dict(zip(y_ticks, map(nice, y_ticks)))

        x_ticks = dict((x_to_h(key), format(value)) for key, value in x_ticks.items())
        y_ticks = dict((y_to_v(key), format(value)) for key, value in y_ticks.items())

        for x, label in x_ticks.items():
            svg += "<text {text} x='{x}' y='{0}' text-anchor='middle'>{label}</text>".format(bottom + marker_size + 0.5 * line_height, **vars())

        for y, label in y_ticks.items():
            svg += "<text {text} text-anchor='middle' transform='translate({0} {y}) rotate(-90)'>{label}</text>".format(left - marker_size - 0.5 * line_height, **vars())

        x_label = format(x_label)
        y_label = format(y_label)

        svg += "<text {text} x='{0}' y='{1}' text-anchor='middle'>{x_label}</text><text {text} text-anchor='middle' transform='translate({2} {3}) rotate(-90)'>{y_label}</text><g stroke='{stroke}' stroke-width='{stroke_width}'>".format(left + 0.5 * inner_width, bottom + x_label_spacing + 0.5 * line_height, left - y_label_spacing - 0.5 * line_height, top + 0.5 * inner_height, **vars())

        for x in x_ticks:
            svg += "<path d='M {x} {bottom} v {marker_size}' />".format(**vars())

        for y in y_ticks:
            svg += "<path d='M {left} {y} h -{marker_size} 0' />".format(**vars())

        svg += "<path d='M {left} {bottom} h {0}' marker-end='url(#arrow)' /><path d='M {left} {bottom} v {1}' marker-end='url(#arrow)' /></g>".format(inner_width + 2 * marker_size, -2 * marker_size - inner_height, right + marker_size, bottom - marker_size, left - marker_size, top - marker_size, **vars())

    svg += after.format(**vars())

    svg += '</svg>'

    if save:
        file = open(name + '.svg', 'w')
        file.write("<?xml version='1.0' encoding='utf-8'?>" + svg)
        file.close()

    return svg
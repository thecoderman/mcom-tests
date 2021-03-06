#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests
from unittestzero import Assert
from pages.desktop.performance import Performance


class TestPerformance:

    @pytest.mark.nondestructive
    def test_footer_section(self, mozwebqa):
        performance_page = Performance(mozwebqa)
        performance_page.go_to_page()
        Assert.contains(performance_page.footer.expected_footer_logo_destination,
                        performance_page.footer.footer_logo_destination)
        Assert.contains(performance_page.footer.expected_footer_logo_img,
                        performance_page.footer.footer_logo_img)
        bad_links = []
        for link in Performance.Footer.footer_links_list:
            url = performance_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))

    @pytest.mark.nondestructive
    def test_tabzilla_links_are_correct(self, mozwebqa):
        performance_page = Performance(mozwebqa)
        performance_page.go_to_page()
        Assert.true(performance_page.header.is_tabzilla_panel_visible)
        performance_page.header.toggle_tabzilla_dropdown()
        bad_links = []
        for link in Performance.Header.tabzilla_links_list:
            url = performance_page.link_destination(link.get('locator'))
            if url.find(link.get('url_suffix')) < 1:
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))

    @pytest.mark.nondestructive
    def test_download_button_section(self, mozwebqa):
        performance_page = Performance(mozwebqa)
        performance_page.go_to_page()
        Assert.true(performance_page.downloadRegion.is_download_link_visible)
        Assert.true(performance_page.downloadRegion.are_secondary_links_visible)

    @pytest.mark.nondestructive
    def test_billboard_links_are_visible(self, mozwebqa):
        performance_page = Performance(mozwebqa)
        performance_page.go_to_page()
        bad_links = []
        for link in performance_page.billboard_links_list:
            if not performance_page.is_element_visible(*link.get('locator')):
                bad_links.append('The link at %s is not visible' % link.get('locator')[1:])
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))

    @pytest.mark.nondestructive
    def test_billboard_link_destinations_are_correct(self, mozwebqa):
        performance_page = Performance(mozwebqa)
        performance_page.go_to_page()
        bad_links = []
        for link in performance_page.billboard_links_list:
            url = performance_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))

    @pytest.mark.nondestructive
    def test_billboard_link_urls_are_valid(self, mozwebqa):
        performance_page = Performance(mozwebqa)
        performance_page.go_to_page()
        bad_urls = []
        for link in performance_page.billboard_links_list:
            url = performance_page.link_destination(link.get('locator'))
            response_code = performance_page.get_response_code(url)
            if response_code != requests.codes.ok:
                bad_urls.append('%s is not a valid url - status code: %s.' % (url, response_code))
        Assert.equal(0, len(bad_urls), '%s bad urls found: ' % len(bad_urls) + ', '.join(bad_urls))

    @pytest.mark.nondestructive
    def test_performance_image_is_correct(self, mozwebqa):
        performance_page = Performance(mozwebqa)
        performance_page.go_to_page()
        src = performance_page.perf_hardware_img_src
        Assert.true(src.endswith('hardware-accel.png'))
        response_code = performance_page.get_response_code(src)
        Assert.equal(response_code, requests.codes.ok, '%s is not a valid url - status code: %s.' % (src, response_code))

    @pytest.mark.nondestructive
    def test_video_srcs_are_valid(self, mozwebqa):
        performance_page = Performance(mozwebqa)
        performance_page.go_to_page()
        bad_srcs = []
        for src in performance_page.video_sources_list:
            response_code = performance_page.get_response_code(src)
            if response_code != requests.codes.ok:
                bad_srcs.append('%s is not a valid url - status code: %s.' % (src, response_code))
        Assert.equal(0, len(bad_srcs), '%s bad urls found: ' % len(bad_srcs) + ', '.join(bad_srcs))
        Assert.true(performance_page.is_video_overlay_visible)

# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LastMatch(models.Model):
    _name = 'last.match'

    home_club_id = fields.Many2one("clubs", string="Home Club", required=True)
    away_club_id = fields.Many2one("clubs", string="Away Club", required=True)

    home_photo = fields.Binary(related='home_club_id.club_image', store=True, readonly=True, string="Home Photo")
    away_photo = fields.Binary(related='away_club_id.club_image', store=True, readonly=True, string="Away Photo")

    home_team_goals = fields.Integer('Home Team Goals')
    away_team_goals = fields.Integer('Away Team Goals')
    date = fields.Datetime('Date')
    stadium = fields.Many2one('stadiums', string='Stadium')
    tournament = fields.Char(string='Tournament')

class NextMatch(models.Model):
    _name = 'next.match'

    home_club_id = fields.Many2one("clubs", string="Home Club", required=True)
    away_club_id = fields.Many2one("clubs", string="Away Club", required=True)

    home_photo = fields.Binary(related='home_club_id.club_image', store=True, readonly=True, string="Home Photo")
    away_photo = fields.Binary(related='away_club_id.club_image', store=True, readonly=True, string="Away Photo")

    date = fields.Datetime('Date')
    stadium = fields.Many2one('stadiums', string='Stadium')
    tournament = fields.Char(string='Tournament', compute='_compute_tournament', store=True)


    @api.model
    def create(self, vals):
        # ვამოწმებთ ბოლო ჩანაწერს ტურნირის ნომრით
        last_tournament = self.search([], order='id desc', limit=1).tournament
        next_number = 1

        if last_tournament and last_tournament.startswith('კრისტალბეთ ეროვნული ლიგა - ტური'):
            try:
                current_num = int(last_tournament.split('ტური')[1])
                next_number = current_num + 1
            except ValueError:
                pass

        # შეზღუდვა 35-მდე
        if next_number > 35:
            raise UserError("მაღაზია, ტურნირის რიცხვები 35-მდე უნდა იყოს. მეტი ჩანაწერი ვერ შეიქმნება.")

        vals['tournament'] = f"კრისტალბეთ ეროვნული ლიგა - ტური {next_number}"
        return super(NextMatch, self).create(vals)
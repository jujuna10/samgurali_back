# -*- coding: utf-8 -*-
from re import search

from odoo import models, fields, api
from odoo.api import onchange


class LastMatch(models.Model):
    _name = 'last.match'
    _rec_name = 'name'

    home_club_id = fields.Many2one("clubs", string="Home Club", required=True)
    away_club_id = fields.Many2one("clubs", string="Away Club", required=True)

    home_photo = fields.Binary(related='home_club_id.club_image', store=True, readonly=True, string="Home Photo")
    away_photo = fields.Binary(related='away_club_id.club_image', store=True, readonly=True, string="Away Photo")

    home_team_goals = fields.Integer('Home Team Goals')
    away_team_goals = fields.Integer('Away Team Goals')
    date = fields.Datetime('Date')
    stadium = fields.Many2one('stadiums', string='Stadium')
    tournament = fields.Char(string='Tournament')

    name = fields.Char(string='Match Name', compute='_compute_name', store=True)

    @api.depends('home_club_id.name', 'away_club_id.name', 'date')
    def _compute_name(self):
        for rec in self:
            home = rec.home_club_id.name or ''
            away = rec.away_club_id.name or ''
            value = f"{home} vs {away}"
            rec.name = value

    samgurali_lineup_ids = fields.One2many('match.lineup', 'match_id', string='Samgurali Lineup')
    photos_ids = fields.One2many('match.photos', 'game_id', string='Match Photos')


    is_samgurali_match = fields.Boolean(
        string='Is Samgurali Involved?',
        compute='_compute_is_samgurali_match',
        store=True
    )

    @api.depends('home_club_id', 'away_club_id')
    def _compute_is_samgurali_match(self):
        for rec in self:
            rec.is_samgurali_match = rec.home_club_id.name == 'სამგურალი' or rec.away_club_id.name == 'სამგურალი'

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         home = record.home_club_id.name or ''
    #         away = record.away_club_id.name or ''
    #         date_str = ''
    #         if record.date:
    #             date_str = record.date.strftime('%Y-%m-%d')
    #         display_name = f"{home} vs {away}"
    #         if date_str:
    #             display_name += f" ({date_str})"
    #         result.append((record.id, display_name))
    #     return result

class MatchLineup(models.Model):
    _name = 'match.lineup'
    _description = 'Match Lineup (Samgurali Players)'

    match_id = fields.Many2one('last.match', string='Match', required=True, ondelete='cascade')
    player_id = fields.Many2one('hr.employee', string='Player', required=True, domain=[('roll', '=', 'footballer')])
    position = fields.Char(string='Position')
    number = fields.Integer(string='Shirt Number')


    minute_in = fields.Char(string='Minute In', help='When player entered the match')
    minute_out = fields.Char(string='Minute Out', help='When player left the match')
    note = fields.Float(string='Comment')
    yellow_cards = fields.Integer(string='Yellow Cards', default=0)
    red_card = fields.Boolean(string='Red Card', default=False)

    goals = fields.Integer(string='Goals', default=0)
    assists = fields.Integer(string='Assists', default=0)
    shots = fields.Integer(string='Shots', default=0)
    shots_on_target = fields.Integer(string='Shots on Target', default=0)
    key_passes = fields.Integer(string='Key Passes', default=0)
    saves = fields.Integer(string='Saves', default=0)
    # goals_conceded = fields.Integer(string='Goals Conceded', default=0)
    clean_sheets = fields.Integer(string='Clean Sheets', default=0)
    tackle = fields.Integer(string='tackle', default=0)
    successful_tackle = fields.Integer(string='successful_tackle', default=0)
    goalkeeper_shots = fields.Integer(string='goalkeeper shots', default=0)




    @api.onchange('player_id')
    def _onchange_player_id(self):
        if self.player_id and self.player_id.position:
            self.position = self.player_id.position

    @api.onchange('yellow_cards')
    def _onchange_yellow_cards(self):
        if self.yellow_cards >= 2:
            self.red_card = True
        else:
            self.red_card = False

    @api.onchange('player_id')
    def _onchange_player_number(self):
        if self.player_id and self.player_id.position:
            self.number = self.player_id.number

class MatchPhotos(models.Model):
    _name = 'match.photos'

    image = fields.Binary(string='Photo')
    game_id = fields.Many2one('last.match', string='Match', required=True, ondelete='cascade')

class NextMatch(models.Model):
    _name = 'next.match'

    home_club_id = fields.Many2one("clubs", string="Home Club", required=True)
    away_club_id = fields.Many2one("clubs", string="Away Club", required=True)

    home_photo = fields.Binary(related='home_club_id.club_image', store=True, readonly=True, string="Home Photo")
    away_photo = fields.Binary(related='away_club_id.club_image', store=True, readonly=True, string="Away Photo")

    date = fields.Datetime('Date')
    stadium = fields.Many2one('stadiums', string='Stadium')
    tournament = fields.Char(string='Tournament', compute='_compute_tournament', store=True)
    link = fields.Char(string='ticket')


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

class Videos(models.Model):
    _name = 'video'

    name = fields.Char(string='video link')
    match = fields.Many2one('last.match', string='Match')
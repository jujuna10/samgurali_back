# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Clubs(models.Model):
    _name = 'clubs'
    _description = 'Clubs'
    _rec_name = 'name'

    name = fields.Char('Club Name', required=True)
    club_image = fields.Binary('Club Image', required=True)



class Stadiums(models.Model):
    _name = 'stadiums'

    name = fields.Char('Stadium Name', required=True)

class Table(models.Model):
    _name = 'table'
    _description = 'League Table'
    _rec_name = 'club_id'

    club_id = fields.Many2one('clubs', string="Club", required=True)
    club_points = fields.Integer('Club Points', default=0)
    goals = fields.Integer('Goals', compute='_onchange_club_id')
    conceded_goals = fields.Integer('Conceded Goals', compute='_onchange_club_id')
    goal_difference = fields.Integer(
        'Goal Difference',
        compute='_onchange_club_id',
        store=True
    )
    matches_played = fields.Integer('Matches Played', default=0)
    wins = fields.Integer('Wins', compute='_onchange_club_id')
    draws = fields.Integer('Draws', compute='_onchange_club_id')
    losses = fields.Integer('Losses', compute='_onchange_club_id')
    club_image = fields.Binary('Club Image')

    @api.depends('club_id')
    def _onchange_club_id(self):
        for rec in self:
            home_match_result = self.env['last.match'].search([('home_club_id', '=', rec.club_id.id)])
            away_match_result = self.env['last.match'].search([('away_club_id', '=', rec.club_id.id)])
            rec.goals = sum(home_match_result.mapped('home_team_goals') + away_match_result.mapped('away_team_goals'))
            rec.conceded_goals = sum(home_match_result.mapped('away_team_goals') + away_match_result.mapped('home_team_goals'))
            rec.goal_difference = rec.goals - rec.conceded_goals
            home_wins = len(home_match_result.filtered(lambda r: r.home_team_goals > r.away_team_goals))
            away_wins = len(away_match_result.filtered(lambda r: r.home_team_goals < r.away_team_goals))
            rec.wins = home_wins + away_wins
            rec.draws = len(away_match_result.filtered(lambda r: r.home_team_goals == r.away_team_goals))
            home_losses = len(home_match_result.filtered(lambda r: r.home_team_goals < r.away_team_goals))
            away_losses = len(away_match_result.filtered(lambda r: r.home_team_goals > r.away_team_goals))
            rec.losses = home_losses + away_losses
            rec.club_points = (home_wins * 3) + (away_wins * 3) + len(away_match_result.filtered(lambda r: r.home_team_goals == r.away_team_goals))


    @api.depends('goals', 'conceded_goals')
    def _compute_goal_difference(self):
        for record in self:
            record.goal_difference = record.goals - record.conceded_goals

    def __str__(self):
        return self.club_id.name if self.club_id else 'No Club'

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    number = fields.Integer(string="number")
    age = fields.Integer(string="age")
    birthday = fields.Date(string="birthday")
    footballer_country = fields.Many2one('fooballer.country', string="Country")
    position = fields.Selection([
        ('goalkeeper', 'Goalkeeper'),
        ('defender', 'Defender'),
        ('midfielder', 'Midfielder'),
        ('attacker', 'Attacker'),
    ], string="position")
    roll = fields.Selection([
        ('footballer', 'Footballer'),
        ('coach','Coach'),
        ('medical staff', 'Medical Staff'),

    ])
    goals = fields.Integer(string="goals", compute='_compute_stats')
    assists = fields.Integer(string="asists", compute='_compute_stats')
    clean_sheets = fields.Integer(string="clean sheets", compute='_compute_stats')

    def _compute_stats(self):
        lineups = self.env['match.lineup'].sudo().search([('player_id', '=', self.id)])
        total_goals = sum(l.goals for l in lineups)
        total_assists = sum(l.assists for l in lineups)
        total_clean_sheets = sum(l.clean_sheets for l in lineups)

        self.goals = total_goals
        self.assists = total_assists
        self.clean_sheets = total_clean_sheets

class News(models.Model):
    _name = 'news'

    title = fields.Char(string="title")
    date = fields.Date(string='date')
    text = fields.Text(string='text')
    image = fields.Binary(string='image')


class FooballerCountry(models.Model):
    _name = 'fooballer.country'

    name = fields.Char(string='Name', required=True)

from werkzeug.urls import url_encode
from datetime import datetime, timedelta
from odoo import http
import random
from odoo.addons.web.controllers.session import Session
from odoo.http import request
import json
from passlib.context import CryptContext
import passlib.context
from odoo.http import Response
import base64


class Table(http.Controller):
    @http.route('/web/table', auth="none", cors='*', methods=['GET'])
    def table(self):
        table_records = request.env['table'].sudo().search([])
        print('dkodkdo')
        result = []
        for i in table_records:
            result.append({
                'id': i.id,
                'points': i.club_points,
                'goals': i.goals,
                'conceded': i.conceded_goals,
                'wins': i.wins,
                'matches_played': i.matches_played,
                'draws': i.draws,
                'losses': i.losses,
                'club_id': i.club_id.name if i.club_id else False,
                'goal_difference': i.goal_difference,
                'image': 'data:image/png;base64,' + i.club_image.decode('utf-8') if i.club_image else False,

            })
        return Response(
            json.dumps({'data': result}),
            content_type='application/json;charset=utf-8',
        )

class News(http.Controller):
    @http.route('/web/main/page/news', auth="none", cors='*', methods=['GET'])
    def news(self):
        news_records = request.env['news'].sudo().search([], limit=2)
        result = []
        for i in news_records:
            result.append({
                'id': i.id,
                'title': i.title,
                'date': i.date.strftime('%Y-%m-%d') if i.date else None,  # აქ ვუშვებთ სტრინგად
                'text': i.text,
            'image': 'data:image/png;base64,' + i.image.decode('utf-8') if i.image else False,

            })
        return Response(
            json.dumps({'data': result}),
            content_type='application/json;charset=utf-8',
        )


class Matches(http.Controller):
    @http.route('/web/lastmatch', auth="none", cors='*', methods=['GET'])
    def last_match(self):
        last_match_records = request.env['last.match'].sudo().search([], limit=1, order='id desc')
        print(last_match_records)
        result = []
        for i in last_match_records:
            result.append({
                'id': i.id,
                'away': i.away_club_id.name if i.away_club_id else None,
                'home': i.home_club_id.name if i.home_club_id else None,
                'away_team_photo': 'data:image/png;base64,' + i.away_photo.decode('utf-8') if i.away_photo else False,
                'home_team_photo': 'data:image/png;base64,' + i.home_photo.decode('utf-8') if i.home_photo else False,
                'away_team_goals': i.away_team_goals,
                'home_team_goals': i.home_team_goals,
                'date': i.date.strftime('%Y-%m-%d %H:%M') if i.date else None,
                'stadium': i.stadium.name if i.stadium else None,
                'tournament': i.tournament,
            })
        return Response(
            json.dumps({'data': result}),
            content_type='application/json;charset=utf-8',
        )

    @http.route('/web/nextmatch', auth="none", cors='*', methods=['GET'])
    def next_match(self):
        next_match_records = request.env['next.match'].sudo().search([], limit=1, order='id desc')
        result = []
        for i in next_match_records:
            result.append({
                'id': i.id,
                'away': i.away_club_id.name if i.away_club_id else None,
                'home': i.home_club_id.name if i.home_club_id else None,
                'away_team_photo': 'data:image/png;base64,' + i.away_photo.decode('utf-8') if i.away_photo else False,
                'home_team_photo': 'data:image/png;base64,' + i.home_photo.decode('utf-8') if i.home_photo else False,
                'date': i.date.strftime('%Y-%m-%d %H:%M') if i.date else None,
                'stadium': i.stadium.name if i.stadium else None,
                'tournament': i.tournament,
            })
        return Response(
            json.dumps({'data': result}),
            content_type='application/json;charset=utf-8',
        )

    @http.route('/web/nextmatches', auth="none", cors='*', methods=['GET'])
    def next_matches(self):
        next_match_records = request.env['next.match'].sudo().search([], limit=3, order='id desc')
        result = []
        for i in next_match_records:
            result.append({
                'id': i.id,
                'away': i.away_club_id.name if i.away_club_id else None,
                'home': i.home_club_id.name if i.home_club_id else None,
                'away_team_photo': 'data:image/png;base64,' + i.away_photo.decode('utf-8') if i.away_photo else False,
                'home_team_photo': 'data:image/png;base64,' + i.home_photo.decode('utf-8') if i.home_photo else False,
                'date': i.date.strftime('%Y-%m-%d %H:%M') if i.date else None,
                'stadium': i.stadium.name if i.stadium else None,
                'tournament': i.tournament,
            })
        return Response(
            json.dumps({'data': result}),
            content_type='application/json;charset=utf-8',
        )

class Footballer(http.Controller):
    @http.route('/web/footballers', auth="public", cors='*', methods=['GET'])
    def footballers(self):
        footballers = request.env['hr.employee'].sudo().search([('roll', '=', 'footballer')],order='id desc')
        result = []
        for i in footballers:
            result.append({
                'id': i.id,
                'number': i.number,
                'birthday': i.birthday,
                'footballer_country': i.footballer_country.name,
                'position': i.position,
                'roll': i.roll,
                'name': i.name,
                'image': 'data:image/png;base64,' + i.image_1920.decode('utf-8'),
                'age': i.age,
            })
        return Response(
            json.dumps({'data': result}),
            content_type='application/json;charset=utf-8',
        )

class Staf(http.Controller):
    @http.route('/web/staf', auth="public", cors='*', methods=['GET'])
    def footballers(self):
        footballers = request.env['hr.employee'].sudo().search([('roll', '=', 'coach')],order='id desc')
        result = []
        for i in footballers:
            result.append({
                'id': i.id,
                'birthday': i.birthday.strftime('%Y-%m-%d') if i.birthday else None,
                'footballer_country': i.footballer_country.name,
                'roll': i.roll,
                'name': i.name,
                # 'image': 'data:image/png;base64,' + i.image_1920.decode('utf-8'),
                'age': i.age,
            })
        return Response(
            json.dumps({'data': result}),
            content_type='application/json;charset=utf-8',
        )

class Doctors(http.Controller):
    @http.route('/web/doctors', auth="public", cors='*', methods=['GET'])
    def footballers(self):
        footballers = request.env['hr.employee'].sudo().search([('roll', '=', 'medical staff')],order='id desc')
        result = []
        for i in footballers:
            result.append({
                'id': i.id,
                'birthday': i.birthday.strftime('%Y-%m-%d') if i.birthday else None,
                'footballer_country': i.footballer_country.name,
                'roll': i.roll,
                'name': i.name,
                # 'image': 'data:image/png;base64,' + i.image_1920.decode('utf-8'),
                'age': i.age,
            })
        return Response(
            json.dumps({'data': result}),
            content_type='application/json;charset=utf-8',
        )

class FootballerInfo(http.Controller):
     @http.route('/web/footballer/<int:footballer_id>', auth="public", methods=['POST'], cors='*', csrf=False)
     def car_info(self,footballer_id, **kwargs):
        footballer = request.env['hr.employee'].sudo().search(
            [('id', '=', footballer_id),
            ('roll', '=', 'footballer')
            ])
        image_data = footballer.image_1920
        if isinstance(image_data, bytes):
            image_data = image_data.decode('utf-8')

        footballer_detail = []
        footballer_detail.append({
            'id': footballer.id,
            'number': footballer.number,
            'birthday': footballer.birthday,
            'footballer_country': footballer.footballer_country.name,
            'position': footballer.position,
            'roll': footballer.roll,
            'name': footballer.name,
            'image': f'data:image/png;base64,{image_data}',
            'age': footballer.age,
        })

        return Response(
            json.dumps({'data': footballer_detail }),
            content_type='application/json;charset=utf-8',
        )



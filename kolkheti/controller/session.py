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
        news_records = request.env['news'].sudo().search([], limit=3)
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

    @http.route('/web/main/page/newses', auth="none", cors='*', methods=['GET'])
    def newes(self):
        news_records = request.env['news'].sudo().search([])
        result = []
        for i in news_records:
            result.append({
                'id': i.id,
                'title': i.title,
                'date': i.date.strftime('%Y-%m-%d') if i.date else None,
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
        next_match_records = request.env['next.match'].sudo().search([], limit=1, order='id asc')
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
                'link': i.link,
            })
        return Response(
            json.dumps({'data': result}),
            content_type='application/json;charset=utf-8',
        )

    @http.route('/web/nextmatches', auth="none", cors='*', methods=['GET'])
    def next_matches(self):
        next_match_records = request.env['next.match'].sudo().search([], limit=3, order='id asc')
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

    @http.route('/web/next/matches/page', auth="none", cors='*', methods=['GET'])
    def next_match_page(self):
        next_match_records = request.env['next.match'].sudo().search([], limit=10, order='id asc')
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
                'link': i.link,
            })
        return Response(
            json.dumps({'data': result}),
            content_type='application/json;charset=utf-8',
        )

    @http.route('/web/last/teams/matches/<string:first>/<string:second>', auth="none", cors='*', methods=['GET'])
    def last_teams_matches(self, first, second):
        domain = ['|',
                  '&', ('home_club_id.name', '=', first), ('away_club_id.name', '=', second),
                  '&', ('home_club_id.name', '=', second), ('away_club_id.name', '=', first)
                  ]
        matches = request.env['last.match'].sudo().search(domain, order='id desc', limit=5)

        data = []
        for i in matches:
            data.append({
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
            json.dumps({'data': data}, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
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

    @http.route('/web/footballer/<int:footballer_id>',auth='public',type='http',methods=['GET', 'OPTIONS'],csrf=False)
    def footballer_info(self, footballer_id, **kwargs):
        # ეს ჰედერები უნდა დაემატოს ყველა პასუხზე
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Content-Type': 'application/json;charset=utf-8',
        }

        # თუ ბრაუზერი აგზავნის OPTIONS მოთხოვნას (preflight), აქვე ვაბრუნებთ პასუხს
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=headers)

        try:
            footballer = request.env['hr.employee'].sudo().search([
                ('id', '=', footballer_id),
                ('roll', '=', 'footballer')
            ], limit=1)

            if not footballer:
                return Response(json.dumps({'error': 'მოთამაშე ვერ მოიძებნა'}), status=404, headers=headers)

            lineups = request.env['match.lineup'].sudo().search([('player_id', '=', footballer_id)])
            matches = request.env['last.match'].sudo().search([])
            team_stats = request.env['match.lineup'].sudo().search([])

            total_goals = sum(l.goals for l in lineups)
            total_assists = sum(l.assists for l in lineups)
            match_played = len(lineups)
            all_match = len(matches)

            samgurali = request.env['table'].sudo().search([
                ('club_id.name', '=', 'სამგურალი')
            ], limit=1)

            total_team_goals = sum(l.goals for l in team_stats)
            total_team_assists = sum(l.assists for l in team_stats)

            image_data = footballer.image_1920
            if isinstance(image_data, bytes):
                image_data = image_data.decode('utf-8')

            footballer_detail = [{
                'id': footballer.id,
                'number': footballer.number,
                'birthday': footballer.birthday,
                'footballer_country': footballer.footballer_country.name,
                'position': footballer.position,
                'roll': footballer.roll,
                'name': footballer.name,
                'image': f'data:image/png;base64,{image_data}',
                'age': footballer.age,
                'footballer_goals': total_goals,
                'footballer_assists': total_assists,
                'total_team_goals': total_team_goals,
                'total_team_assists': total_team_assists,
                'match_played': match_played,
                'all_match': all_match,
            }]

            return Response(json.dumps({'data': footballer_detail}), headers=headers)

        except Exception as e:
            return Response(json.dumps({'error': str(e)})
    )

    @http.route('/web/top/scoreer', auth="public", methods=['GET'], cors='*', csrf=False)
    def top_scorers(self, **kwargs):
        footballers = request.env['hr.employee'].sudo().search([('roll', '=', 'footballer')])

        player_stats = []

        for player in footballers:
            lineups = request.env['match.lineup'].sudo().search([('player_id', '=', player.id)])

            total_goals = sum(lineup.goals for lineup in lineups)
            total_assists = sum(lineup.assists for lineup in lineups)
            match_played = len(lineups)

            image_data = player.image_1920
            if isinstance(image_data, bytes):
                image_data = image_data.decode('utf-8')

            player_stats.append({
                'id': player.id,
                'number': player.number,
                'position': player.position,
                'name': player.name,
                'image': f'data:image/png;base64,{image_data}',
                'footballer_goals': total_goals,
                'footballer_assists': total_assists,
                'match_played': match_played,
            })

        sorted_players = sorted(player_stats, key=lambda x: x['footballer_goals'], reverse=True)

        top_three = sorted_players[:3]

        return Response(
            json.dumps({'data': top_three}),
            content_type='application/json;charset=utf-8',
    )

    @http.route('/web/videos', auth="public", methods=['GET'], cors='*', csrf=False)
    def videos(self, **kwargs):
        video_records = request.env['video'].sudo().search([], limit=4)

        videos = []

        for video in video_records:
            videos.append({
                'id': video.id,
                'link': video.name,
                'match_id': video.match.name if video.match else False,
            })

        return Response(
            json.dumps({'data': videos}),
            content_type='application/json;charset=utf-8',
        )

    @http.route('/web/photos', auth="public", methods=['GET'], cors='*', csrf=False)
    def photos(self, **kwargs):
        matches = request.env['last.match'].sudo().search([], limit=4, order='id desc')
        data = []

        for match in matches:
            match_photos = []
            for photo in match.photos_ids:
                # მოაშორე b'...' ფორმატირება
                image_data = photo.image
                if isinstance(image_data, bytes):
                    image_data = image_data.decode('utf-8')
                elif isinstance(image_data, str) and image_data.startswith("b'"):
                    image_data = image_data[2:-1]  # მოაშორე b' და ბოლო '

                match_photos.append({
                    'image': f"data:image/png;base64,{image_data}" if image_data else None
                })

            data.append({
                'id': match.id,
                'match_name': match.name,
                'photos': match_photos
            })

        return Response(
            json.dumps({'data': data}),
            content_type='application/json;charset=utf-8',
        )

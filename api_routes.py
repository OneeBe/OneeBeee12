
from flask import jsonify
from app import app
from models import Player

@app.route('/api/leaderboard')
def api_leaderboard():
    """API endpoint for leaderboard data with fallback"""
    try:
        sort_by = request.args.get('sort', 'experience')
        limit = min(int(request.args.get('limit', 50)), 100)
        
        players = Player.get_leaderboard(sort_by=sort_by, limit=limit) or []
        
        # Convert players to dict format
        players_data = []
        for player in players:
            players_data.append({
                'id': player.id,
                'nickname': player.nickname,
                'level': player.level,
                'experience': player.experience,
                'kills': player.kills,
                'deaths': player.deaths,
                'wins': player.wins,
                'games_played': player.games_played,
                'kd_ratio': player.kd_ratio,
                'win_rate': player.win_rate
            })
        
        return jsonify({
            'success': True,
            'players': players_data,
            'total': len(players_data)
        })
    except Exception as e:
        app.logger.error(f"Error in API leaderboard: {e}")
        return jsonify({
            'success': False,
            'players': [],
            'total': 0,
            'error': 'Failed to load leaderboard data'
        }), 200  # Still return 200 with empty data
@app.route('/api/leaderboard')
def api_leaderboard():
    """API endpoint for modern leaderboard data"""
    try:
        sort_by = request.args.get('sort', 'experience')
        limit = min(int(request.args.get('limit', 50)), 100)
        offset = max(0, int(request.args.get('offset', 0)))
        format_type = request.args.get('format', 'standard')
        
        players = Player.get_leaderboard(sort_by=sort_by, limit=limit, offset=offset)
        
        if format_type == 'modern':
            players_data = []
            for player in players:
                # Get admin role
                admin_role_data = None
                admin_role = player.active_admin_role
                if admin_role:
                    admin_role_data = {
                        'name': admin_role.name,
                        'color': admin_role.color,
                        'has_gradient': admin_role.has_gradient,
                        'gradient_start': admin_role.gradient_start,
                        'gradient_end': admin_role.gradient_end,
                        'gradient_animated': admin_role.gradient_animated,
                        'emoji': admin_role.emoji,
                        'emoji_class': admin_role.emoji_class,
                        'emoji_url': admin_role.emoji_url
                    }
                
                # Get nickname gradient
                nickname_gradient = player.nickname_gradient
                
                player_data = {
                    'id': player.id,
                    'nickname': player.nickname,
                    'level': player.level,
                    'experience': player.experience,
                    'kills': player.kills,
                    'final_kills': player.final_kills,
                    'deaths': player.deaths,
                    'beds_broken': player.beds_broken,
                    'wins': player.wins,
                    'games_played': player.games_played,
                    'kd_ratio': player.kd_ratio,
                    'win_rate': player.win_rate,
                    'role': player.role,
                    'custom_role': player.custom_role,
                    'custom_role_purchased': player.custom_role_purchased,
                    'custom_role_color': player.custom_role_color,
                    'custom_role_gradient': player.custom_role_gradient,
                    'custom_role_animated': player.custom_role_animated,
                    'custom_role_emoji': player.custom_role_emoji,
                    'admin_role': admin_role_data,
                    'nickname_gradient': nickname_gradient,
                    'skin_url': player.minecraft_skin_url
                }
                players_data.append(player_data)
            
            return jsonify({
                'success': True,
                'players': players_data,
                'total': len(players_data),
                'sort_by': sort_by
            })
        else:
            # Standard format for backwards compatibility
            players_data = [
                {
                    'id': p.id,
                    'nickname': p.nickname,
                    'level': p.level,
                    'experience': p.experience,
                    'kills': p.kills,
                    'final_kills': p.final_kills,
                    'deaths': p.deaths,
                    'beds_broken': p.beds_broken,
                    'wins': p.wins,
                    'kd_ratio': p.kd_ratio,
                    'role': p.display_role
                }
                for p in players
            ]
            
            return jsonify({
                'success': True,
                'players': players_data,
                'total': len(players_data)
            })
            
    except Exception as e:
        app.logger.error(f"Error in leaderboard API: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

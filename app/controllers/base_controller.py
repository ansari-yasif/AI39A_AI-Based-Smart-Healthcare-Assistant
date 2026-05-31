"""app/controllers/base_controller.py — Shared response helpers"""
from flask import render_template, redirect, url_for, flash, jsonify, request, session

class BaseController:
    @staticmethod
    def render(tpl, **ctx): return render_template(tpl, **ctx)
    @staticmethod
    def redirect_to(ep, **kw): return redirect(url_for(ep, **kw))
    @staticmethod
    def flash_ok(msg): flash(msg, 'success')
    @staticmethod
    def flash_err(msg): flash(msg, 'error')
    @staticmethod
    def flash_warn(msg): flash(msg, 'warning')
    @staticmethod
    def json_ok(data=None, msg='OK'): return jsonify({'status':'ok','message':msg,'data':data})
    @staticmethod
    def json_err(msg, code=400): return jsonify({'status':'error','message':msg}), code
    @staticmethod
    def uid(): return session.get('user_id')
    @staticmethod
    def form(k, default=''): return request.form.get(k, default)
    @staticmethod
    def form_int(k, default=0):
        try: return int(request.form.get(k, default))
        except: return default
    @staticmethod
    def form_float(k, default=0.0):
        try: return float(request.form.get(k, default))
        except: return default

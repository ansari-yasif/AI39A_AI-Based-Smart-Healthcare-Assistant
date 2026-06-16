"""app/controllers/health_controller.py — Sleep, Mood, Weight, Workout trackers"""
from datetime import date, timedelta
from flask import request, redirect, url_for, flash
from app.controllers.base_controller import BaseController
from app.models.sleep import SleepModel
from app.models.mood import MoodModel
from app.models.weight import WeightModel
from app.models.workout import WorkoutModel
from app.helpers import today_str

MOOD_ICONS = {
    'happy': '😊', 'energetic': '⚡', 'calm': '😌', 'focused': '🎯',
    'excited': '🤩', 'tired': '😴', 'stressed': '😰',
    'anxious': '😬', 'sad': '😢', 'angry': '😤',
}


class HealthController(BaseController):

    # ──────────────────────────────────────────────────────────────────────
    # SLEEP TRACKER
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def sleep_index(cls):
        uid   = cls.uid()
        today = today_str()
        entry  = SleepModel.get_by_date(uid, today)
        recent = SleepModel.recent(uid, 14)

        labels, hours_data = [], []
        for i in range(6, -1, -1):
            d = (date.today() - timedelta(days=i)).isoformat()
            row = SleepModel.get_by_date(uid, d)
            labels.append(d[5:])
            hours_data.append(
                round(float(row['hours_slept']), 1) if row and row.get('hours_slept') else 0
            )

        logged = [h for h in hours_data if h > 0]
        avg = round(sum(logged) / len(logged), 1) if logged else 0.0

        return cls.render('health/sleep_tracker.html',
            entry=entry, recent=recent,
            labels=labels, hours_data=hours_data,
            avg=avg, today=today,
        )

    @classmethod
    def sleep_log(cls):
        uid      = cls.uid()
        today    = today_str()
        bedtime  = request.form.get('bedtime', '') or None
        wake     = request.form.get('wake', '') or None
        notes    = request.form.get('notes', '')
        log_date = request.form.get('log_date', today)
        quality  = int(request.form.get('quality', 3))
        try:
            hours = float(request.form.get('hours', 0) or 0)
        except ValueError:
            hours = 0.0
        try:
            SleepModel.log(uid, log_date, bedtime, wake, hours, quality, notes)
            flash('Sleep logged!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        return redirect(url_for('health.sleep_index'))

    @classmethod
    def sleep_delete(cls, sid):
        uid = cls.uid()
        SleepModel.delete(sid, uid)
        flash('Entry removed.', 'info')
        return redirect(url_for('health.sleep_index'))

    # ──────────────────────────────────────────────────────────────────────
    # MOOD TRACKER
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def mood_index(cls):
        uid   = cls.uid()
        today = today_str()
        entry  = MoodModel.get_by_date(uid, today)
        recent = MoodModel.recent(uid, 14)

        start30 = (date.today() - timedelta(days=30)).isoformat()
        freq = MoodModel.frequency(uid, start30, today) or []

        return cls.render('health/mood_tracker.html',
            entry=entry, recent=recent,
            freq=freq, mood_icons=MOOD_ICONS,
            today=today,
        )

    @classmethod
    def mood_log(cls):
        uid      = cls.uid()
        today    = today_str()
        mood     = request.form.get('mood', 'calm')
        notes    = request.form.get('notes', '')
        log_date = request.form.get('log_date', today)
        try:
            energy = int(request.form.get('energy', 3))
        except ValueError:
            energy = 3
        try:
            MoodModel.log(uid, log_date, mood, energy, notes)
            flash('Mood logged!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        return redirect(url_for('health.mood_index'))

    # ──────────────────────────────────────────────────────────────────────
    # WEIGHT TRACKER
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def weight_index(cls):
        uid    = cls.uid()
        today  = today_str()
        entry  = WeightModel.get_by_date(uid, today)
        recent = WeightModel.recent(uid, 30) or []

        labels, weight_data = [], []
        for row in list(reversed(list(WeightModel.recent(uid, 14) or []))):
            labels.append(str(row['log_date'])[5:])
            weight_data.append(float(row['weight_kg']))

        latest  = WeightModel.latest(uid)
        cur_w   = round(float(latest['weight_kg']), 1) if latest else 0
        weights = [float(r['weight_kg']) for r in recent if r.get('weight_kg')]
        min_w   = round(min(weights), 1) if weights else 0
        max_w   = round(max(weights), 1) if weights else 0

        return cls.render('health/weight_tracker.html',
            entry=entry, recent=recent,
            labels=labels, weight_data=weight_data,
            current_weight=cur_w, min_w=min_w, max_w=max_w,
            today=today,
        )

    @classmethod
    def weight_log(cls):
        uid      = cls.uid()
        today    = today_str()
        notes    = request.form.get('notes', '')
        log_date = request.form.get('log_date', today)
        try:
            weight = float(request.form.get('weight_kg', 0) or 0)
            if weight <= 0:
                raise ValueError('Weight must be positive')
            WeightModel.log(uid, log_date, weight, notes)
            flash(f'Weight {weight} kg logged!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        return redirect(url_for('health.weight_index'))

    # ──────────────────────────────────────────────────────────────────────
    # WORKOUT TRACKER
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def workout_index(cls):
        uid   = cls.uid()
        today = today_str()
        start_week = (date.today() - timedelta(days=date.today().weekday())).isoformat()
        wkt    = WorkoutModel.week_total(uid, start_week, today)
        recent = WorkoutModel.recent(uid, 10) or []
        TYPES  = ['Running', 'Walking', 'Cycling', 'Swimming', 'Gym / Weights',
                  'Yoga', 'HIIT', 'Sports', 'Dancing', 'Other']
        return cls.render('health/workout_tracker.html',
            wkt=wkt, recent=recent, workout_types=TYPES, today=today,
        )

    @classmethod
    def workout_log(cls):
        uid      = cls.uid()
        today    = today_str()
        wtype    = request.form.get('workout_type', 'Other')
        notes    = request.form.get('notes', '')
        log_date = request.form.get('log_date', today)
        try:
            duration = int(request.form.get('duration', 0) or 0)
            burned   = int(request.form.get('calories_burned', 0) or 0)
            WorkoutModel.log(uid, wtype, duration, burned, notes, log_date)
            flash(f'{wtype} logged!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        return redirect(url_for('health.workout_index'))

    @classmethod
    def workout_delete(cls, wid):
        uid = cls.uid()
        WorkoutModel.delete(wid, uid)
        flash('Workout removed.', 'info')
        return redirect(url_for('health.workout_index'))

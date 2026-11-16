from flask import Blueprint, g, jsonify
from sqlalchemy import column, func, select, table

from . import db
from .security import require_auth

analytics = Blueprint("analytics", __name__, url_prefix="/analytics")

# The database view has one row per deviation and resolves the lookup names.
details = table("deviation_details", *map(column, (
    "concern_type", "severity", "status", "created_at", "assigned_to", "deadline",
)))


def visible_deviations(*columns):
    query = select(*columns).select_from(details)
    if g.user.role == "worker":
        query = query.where(details.c.assigned_to == g.user.user_id)
    return query


def grouped_counts(group):
    query = visible_deviations(group, func.count()).where(group.is_not(None))
    return db.session.execute(query.group_by(group).order_by(group))


@analytics.get("/summary")
@require_auth()
def summary():
    status = details.c.status
    query = visible_deviations(
        func.count().label("total_deviations"),
        func.count().filter(status == "Open").label("open"),
        func.count().filter(status == "In Progress").label("in_progress"),
        func.count().filter(status == "Closed").label("closed"),
        func.count().filter(status != "Closed", details.c.deadline < func.current_date()).label("overdue"),
    )
    return jsonify(dict(db.session.execute(query).mappings().one()))


@analytics.get("/by-type")
@require_auth()
def by_type():
    counts = {}
    for name, count in grouped_counts(details.c.concern_type):
        if name == "Quality Issue":
            name = "Quality"
        counts[name] = counts.get(name, 0) + count
    return jsonify([{"type": name, "count": counts[name]} for name in sorted(counts)])


@analytics.get("/by-severity")
@require_auth()
def by_severity():
    return jsonify([{"severity": name, "count": count}
                    for name, count in grouped_counts(details.c.severity)])


@analytics.get("/by-status")
@require_auth()
def by_status():
    counts = dict(grouped_counts(details.c.status).all())
    return jsonify([{"status": status, "count": counts.get(status, 0)}
                    for status in ("Open", "In Progress", "Closed")])


@analytics.get("/over-time")
@require_auth()
def over_time():
    return jsonify([{"date": str(day), "count": count}
                    for day, count in grouped_counts(func.date(details.c.created_at))])

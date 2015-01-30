CREATE TABLE landolt(
 name varchar(11),
 ra double precision,
 dec double precision,
 vmag real,
 bv real,
 ub real,
 vr real,
 ri real,
 vi real,
 nobs integer,
 nnig integer,
 e_vmag real,
 e_bv real,
 e_ub real,
 e_vr real,
 e_ri real,
 e_vi real,
 coord point,
 PRIMARY KEY (name)
);


select frames.objid, max(airmass) "airmass", count(star) "nstar", avg(mag_auto-vmag) "o-c mag", stddev_pop(mag_auto-vmag) "sigma"
from frames, phot, landolt
where object like 'Landolt%'
and filter='V'
and frames.objid=phot.objid
and landolt.coord <@ circle(phot.coord,3./3600.)
and frames.objid like '2015012%'
group by frames.objid;

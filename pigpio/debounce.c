
/* Autogenerated by /usr/bin/instcomp on Thu May 11 21:31:06 2017 -- do not edit */

#include "rtapi.h"
#ifdef RTAPI
#include "rtapi_app.h"
#endif
#include "rtapi_string.h"
#include "rtapi_errno.h"
#include "hal.h"
#include "hal_priv.h"
#include "hal_accessor.h"
#include "hal_internal.h"

static int comp_id;


static char *compname = "debounce";

#ifdef MODULE_INFO
MODULE_INFO(machinekit, "component:debounce:Debounce filter for Machinekit HAL");
MODULE_INFO(machinekit, "pin:#.in:bit:pincount:in::None");
MODULE_INFO(machinekit, "pin:#.out:bit:pincount:out::None");
MODULE_INFO(machinekit, "pin:#.state:s32:pincount:io::None");
MODULE_INFO(machinekit, "pin:delay:s32:None:io::5");
MODULE_INFO(machinekit, "instanceparam:pincount:int::8");
MODULE_INFO(machinekit, "license:GPL");
MODULE_INFO(machinekit, "author:John Kasunich, adapted by ArcEye");
MODULE_INFO(machinekit, "funct:_:1:");
MODULE_LICENSE("GPL");
#endif // MODULE_INFO
RTAPI_TAG(HAL,HC_INSTANTIABLE);


#define MAXCOUNT 16
#define DEFAULTCOUNT 8

static int pincount = 8;
RTAPI_IP_INT(pincount, "");

struct inst_data
    {
    hal_bit_t *_in[16];
    hal_bit_t *_out[16];
    hal_s32_t *_state[16];
    hal_s32_t *delay;
    int local_argc;
    char **local_argv;
    int local_pincount;
    };

static int maxpins __attribute__((unused)) = 16;
static int debounce_(void *arg, const hal_funct_args_t *fa);

static int instantiate(const int argc, const char**argv);

static int delete(const char *name, void *inst, const int inst_size);

#undef TRUE
#undef FALSE
#undef true
#define true (1)
#undef false
#define false (0)

static int export_halobjs(struct inst_data *ip, int owner_id, const char *name, const int argc, const char **argv)
{
    char buf[HAL_NAME_LEN + 1];
    int r = 0;
    int j __attribute__((unused)) = 0;
    int z __attribute__((unused)) = 0;
    z = pincount;
    if(z > maxpins)
       z = maxpins;
    for(j=0; j < z; j++)
        {
        r = hal_pin_bit_newf(HAL_IN, &(ip->_in[j]), owner_id,
            "%s.%01d.in", name, j);
        if(r != 0) return r;
        }

    z = pincount;
    if(z > maxpins)
       z = maxpins;
    for(j=0; j < z; j++)
        {
        r = hal_pin_bit_newf(HAL_OUT, &(ip->_out[j]), owner_id,
            "%s.%01d.out", name, j);
        if(r != 0) return r;
        }

    z = pincount;
    if(z > maxpins)
       z = maxpins;
    for(j=0; j < z; j++)
        {
        r = hal_pin_s32_newf(HAL_IO, &(ip->_state[j]), owner_id,
            "%s.%01d.state", name, j);
        if(r != 0) return r;
        }

    r = hal_pin_s32_newf(HAL_IO, &(ip->delay), owner_id,
            "%s.delay", name);
    if(r != 0) return r;

    *(ip->delay) = 5;

// if not set by instantiate() set to default
    if(! ip->local_pincount || ip->local_pincount == -1)
         ip->local_pincount = DEFAULTCOUNT;

    hal_print_msg(RTAPI_MSG_DBG,"export_halobjs() ip->local_pincount set to %d", ip->local_pincount);


    ip->local_argv = halg_dupargv(1, argc, argv);

    ip->local_argc = argc;


    // exporting an extended thread function:
    hal_export_xfunct_args_t __xf = 
        {
        .type = FS_XTHREADFUNC,
        .funct.x = debounce_,
        .arg = ip,
        .uses_fp = 1,
        .reentrant = 0,
        .owner_id = owner_id
        };

    rtapi_snprintf(buf, sizeof(buf),"%s.funct", name);
    r = hal_export_xfunctf(&__xf, buf, name);
    if(r != 0)
        return r;
    return 0;
}

// constructor - init all HAL pins, funct etc here
static int instantiate(const int argc, const char**argv)
{
struct inst_data *ip;
// argv[0]: component name
const char *name = argv[1];
int r;

// allocate a named instance, and some HAL memory for the instance data
int inst_id = hal_inst_create(name, comp_id, sizeof(struct inst_data), (void **)&ip);

    if (inst_id < 0)
        return -1;

// here ip is guaranteed to point to a blob of HAL memory of size sizeof(struct inst_data).
    hal_print_msg(RTAPI_MSG_DBG,"%s inst=%s argc=%d",__FUNCTION__, name, argc);

// Debug print of params and values
    hal_print_msg(RTAPI_MSG_DBG,"%s: int instance param: %s=%d",__FUNCTION__,"pincount", pincount);
//  if pincount=NN is passed, set local variable here, if not set to default
    int pin_param_value = pincount;
    if((pin_param_value == -1) || (pin_param_value == 0))
        pin_param_value = DEFAULTCOUNT;
    else if((pin_param_value > 0) && (pin_param_value > MAXCOUNT))
        pin_param_value = MAXCOUNT;
    ip->local_pincount = pincount = pin_param_value;
    hal_print_msg(RTAPI_MSG_DBG,"ip->local_pincount set to %d", pin_param_value);

// These pins - pin_ptrs- functs will be owned by the instance, and can be separately exited with delinst
    r = export_halobjs(ip, inst_id, name, argc, argv);
//reset pincount to -1 so that instantiation without it will result in DEFAULTCOUNT
    pincount = -1;

    return r;
}

int rtapi_app_main(void)
{
    comp_id = hal_xinit(TYPE_RT, 0, 0, instantiate, delete, compname);

    if (comp_id < 0)

        return -1;

    hal_ready(comp_id);

    return 0;
}

void rtapi_app_exit(void)
{
    hal_exit(comp_id);
}

// Custom destructor - delete()
// pins, pin_ptrs, and functs are automatically deallocated regardless if a
// destructor is used or not (see below)
//
// Some objects like vtables, rings, threads are not owned by a component
// interaction with such objects may require a custom destructor for
// cleanup actions
// Also allocated memory that hal_lib will know nothing about ie local_argv
//
// NB: if a customer destructor is used, it is called
// - after the instance's functs have been removed from their respective threads
//   (so a thread funct call cannot interact with the destructor any more)
// - any pins and params of this instance are still intact when the destructor is
//   called, and they are automatically destroyed by the HAL library once the
//   destructor returns


static int delete(const char *name, void *inst, const int inst_size)
{

    struct inst_data *ip = inst;

    HALDBG("Entering delete() : inst=%s size=%d %p local_argv = %p\n", name, inst_size, inst, ip->local_argv);

    HALDBG("Before free ip->local_argv[0] = %s\n", ip->local_argv[0]);

   	halg_free_argv(1, ip->local_argv);

    HALDBG("Now ip->local_argv[0] = %s\n", ip->local_argv[0]);

    return 0;

}


#undef FUNCTION
#define FUNCTION(name) static int debounce_(void *arg, const hal_funct_args_t *fa)
#undef fperiod
#define fperiod (period * 1e-9)
#undef _in
#define _in(i) (0+*(ip->_in[i]))
#undef _out
#define _out(i) (*(ip->_out[i]))
#undef _state
#define _state(i) (*(ip->_state[i]))
#undef delay
#define delay (*ip->delay)
#undef local_pincount
#define local_pincount (ip->local_pincount)
#undef local_argc
#define local_argc (ip->local_argc)
#undef local_argv
#define local_argv(i) (ip->local_argv[i])


#line 20 "debounce.icomp"

FUNCTION(_)
{
long period __attribute__((unused)) = fa_period(fa);
struct inst_data *ip __attribute__((unused)) = arg;

hal_s32_t n;

    // first make sure delay is sane
    if (delay < 0)
        delay = 1;

    // loop through filters
    for (n = 0; n < local_pincount; n++)
        {
        if(_in(n))
            {
            /* input true, is state at threshold? */
            if (_state(n) < delay)
                _state(n)++;
            else
                _out(n) = true;
            }
        else
            {
            if (_state(n) > 0)
                _state(n)--;
            else
                _out(n) = false;
            }
        }
    return 0;
}


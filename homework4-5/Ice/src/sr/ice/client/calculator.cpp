//
// Copyright (c) ZeroC, Inc. All rights reserved.
//
//
// Ice version 3.7.10
//
// <auto-generated>
//
// Generated from file `calculator.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

#include "calculator.h"
#include <IceUtil/PushDisableWarnings.h>
#include <Ice/LocalException.h>
#include <Ice/ValueFactory.h>
#include <Ice/OutgoingAsync.h>
#include <Ice/InputStream.h>
#include <Ice/OutputStream.h>
#include <Ice/LocalException.h>
#include <IceUtil/PopDisableWarnings.h>

#if defined(_MSC_VER)
#   pragma warning(disable:4458) // declaration of ... hides class member
#elif defined(__clang__)
#   pragma clang diagnostic ignored "-Wshadow"
#elif defined(__GNUC__)
#   pragma GCC diagnostic ignored "-Wshadow"
#endif

#ifndef ICE_IGNORE_VERSION
#   if ICE_INT_VERSION / 100 != 307
#       error Ice version mismatch!
#   endif
#   if ICE_INT_VERSION % 100 >= 50
#       error Beta header file detected
#   endif
#   if ICE_INT_VERSION % 100 < 10
#       error Ice patch level mismatch!
#   endif
#endif

#ifdef ICE_CPP11_MAPPING // C++11 mapping

namespace
{

const ::IceInternal::DefaultUserExceptionFactoryInit<::Demo::NoInput> iceC_Demo_NoInput_init("::Demo::NoInput");

const ::std::string iceC_Demo_Calc_ids[2] =
{
    "::Demo::Calc",
    "::Ice::Object"
};
const ::std::string iceC_Demo_Calc_ops[] =
{
    "add",
    "ice_id",
    "ice_ids",
    "ice_isA",
    "ice_ping",
    "op",
    "subtract"
};
const ::std::string iceC_Demo_Calc_add_name = "add";
const ::std::string iceC_Demo_Calc_subtract_name = "subtract";
const ::std::string iceC_Demo_Calc_op_name = "op";

}

Demo::NoInput::~NoInput()
{
}

const ::std::string&
Demo::NoInput::ice_staticId()
{
    static const ::std::string typeId = "::Demo::NoInput";
    return typeId;
}

bool
Demo::Calc::ice_isA(::std::string s, const ::Ice::Current&) const
{
    return ::std::binary_search(iceC_Demo_Calc_ids, iceC_Demo_Calc_ids + 2, s);
}

::std::vector<::std::string>
Demo::Calc::ice_ids(const ::Ice::Current&) const
{
    return ::std::vector<::std::string>(&iceC_Demo_Calc_ids[0], &iceC_Demo_Calc_ids[2]);
}

::std::string
Demo::Calc::ice_id(const ::Ice::Current&) const
{
    return ice_staticId();
}

const ::std::string&
Demo::Calc::ice_staticId()
{
    static const ::std::string typeId = "::Demo::Calc";
    return typeId;
}

/// \cond INTERNAL
bool
Demo::Calc::_iceD_add(::IceInternal::Incoming& inS, const ::Ice::Current& current)
{
    _iceCheckMode(::Ice::OperationMode::Normal, current.mode);
    auto istr = inS.startReadParams();
    int iceP_a;
    int iceP_b;
    istr->readAll(iceP_a, iceP_b);
    inS.endReadParams();
    long long int ret = this->add(iceP_a, iceP_b, current);
    auto ostr = inS.startWriteParams();
    ostr->writeAll(ret);
    inS.endWriteParams();
    return true;
}
/// \endcond

/// \cond INTERNAL
bool
Demo::Calc::_iceD_subtract(::IceInternal::Incoming& inS, const ::Ice::Current& current)
{
    _iceCheckMode(::Ice::OperationMode::Normal, current.mode);
    auto istr = inS.startReadParams();
    int iceP_a;
    int iceP_b;
    istr->readAll(iceP_a, iceP_b);
    inS.endReadParams();
    long long int ret = this->subtract(iceP_a, iceP_b, current);
    auto ostr = inS.startWriteParams();
    ostr->writeAll(ret);
    inS.endWriteParams();
    return true;
}
/// \endcond

/// \cond INTERNAL
bool
Demo::Calc::_iceD_op(::IceInternal::Incoming& inS, const ::Ice::Current& current)
{
    _iceCheckMode(::Ice::OperationMode::Normal, current.mode);
    auto istr = inS.startReadParams();
    A iceP_a1;
    short iceP_b1;
    istr->readAll(iceP_a1, iceP_b1);
    inS.endReadParams();
    this->op(::std::move(iceP_a1), iceP_b1, current);
    inS.writeEmptyParams();
    return true;
}
/// \endcond

/// \cond INTERNAL
bool
Demo::Calc::_iceDispatch(::IceInternal::Incoming& in, const ::Ice::Current& current)
{
    ::std::pair<const ::std::string*, const ::std::string*> r = ::std::equal_range(iceC_Demo_Calc_ops, iceC_Demo_Calc_ops + 7, current.operation);
    if(r.first == r.second)
    {
        throw ::Ice::OperationNotExistException(__FILE__, __LINE__, current.id, current.facet, current.operation);
    }

    switch(r.first - iceC_Demo_Calc_ops)
    {
        case 0:
        {
            return _iceD_add(in, current);
        }
        case 1:
        {
            return _iceD_ice_id(in, current);
        }
        case 2:
        {
            return _iceD_ice_ids(in, current);
        }
        case 3:
        {
            return _iceD_ice_isA(in, current);
        }
        case 4:
        {
            return _iceD_ice_ping(in, current);
        }
        case 5:
        {
            return _iceD_op(in, current);
        }
        case 6:
        {
            return _iceD_subtract(in, current);
        }
        default:
        {
            assert(false);
            throw ::Ice::OperationNotExistException(__FILE__, __LINE__, current.id, current.facet, current.operation);
        }
    }
}
/// \endcond

/// \cond INTERNAL
void
Demo::CalcPrx::_iceI_add(const ::std::shared_ptr<::IceInternal::OutgoingAsyncT<long long int>>& outAsync, int iceP_a, int iceP_b, const ::Ice::Context& context)
{
    _checkTwowayOnly(iceC_Demo_Calc_add_name);
    outAsync->invoke(iceC_Demo_Calc_add_name, ::Ice::OperationMode::Normal, ::Ice::FormatType::DefaultFormat, context,
        [&](::Ice::OutputStream* ostr)
        {
            ostr->writeAll(iceP_a, iceP_b);
        },
        nullptr);
}
/// \endcond

/// \cond INTERNAL
void
Demo::CalcPrx::_iceI_subtract(const ::std::shared_ptr<::IceInternal::OutgoingAsyncT<long long int>>& outAsync, int iceP_a, int iceP_b, const ::Ice::Context& context)
{
    _checkTwowayOnly(iceC_Demo_Calc_subtract_name);
    outAsync->invoke(iceC_Demo_Calc_subtract_name, ::Ice::OperationMode::Normal, ::Ice::FormatType::DefaultFormat, context,
        [&](::Ice::OutputStream* ostr)
        {
            ostr->writeAll(iceP_a, iceP_b);
        },
        nullptr);
}
/// \endcond

/// \cond INTERNAL
void
Demo::CalcPrx::_iceI_op(const ::std::shared_ptr<::IceInternal::OutgoingAsyncT<void>>& outAsync, const A& iceP_a1, short iceP_b1, const ::Ice::Context& context)
{
    outAsync->invoke(iceC_Demo_Calc_op_name, ::Ice::OperationMode::Normal, ::Ice::FormatType::DefaultFormat, context,
        [&](::Ice::OutputStream* ostr)
        {
            ostr->writeAll(iceP_a1, iceP_b1);
        },
        nullptr);
}
/// \endcond

/// \cond INTERNAL
::std::shared_ptr<::Ice::ObjectPrx>
Demo::CalcPrx::_newInstance() const
{
    return ::IceInternal::createProxy<CalcPrx>();
}
/// \endcond

const ::std::string&
Demo::CalcPrx::ice_staticId()
{
    return Calc::ice_staticId();
}

namespace Ice
{
}

#else // C++98 mapping

namespace
{

const ::std::string iceC_Demo_Calc_add_name = "add";

const ::std::string iceC_Demo_Calc_subtract_name = "subtract";

const ::std::string iceC_Demo_Calc_op_name = "op";

}

namespace
{

const ::IceInternal::DefaultUserExceptionFactoryInit< ::Demo::NoInput> iceC_Demo_NoInput_init("::Demo::NoInput");

}

#ifdef ICE_CPP11_COMPILER
Demo::NoInput::~NoInput()
{
}
#else
Demo::NoInput::~NoInput() throw()
{
}
#endif

::std::string
Demo::NoInput::ice_id() const
{
    return "::Demo::NoInput";
}

Demo::NoInput*
Demo::NoInput::ice_clone() const
{
    return new NoInput(*this);
}

void
Demo::NoInput::ice_throw() const
{
    throw *this;
}

/// \cond STREAM
void
Demo::NoInput::_writeImpl(::Ice::OutputStream* ostr) const
{
    ostr->startSlice("::Demo::NoInput", -1, true);
    ::Ice::StreamWriter< NoInput, ::Ice::OutputStream>::write(ostr, *this);
    ostr->endSlice();
}

void
Demo::NoInput::_readImpl(::Ice::InputStream* istr)
{
    istr->startSlice();
    ::Ice::StreamReader< NoInput, ::Ice::InputStream>::read(istr, *this);
    istr->endSlice();
}
/// \endcond

/// \cond INTERNAL
::IceProxy::Ice::Object* ::IceProxy::Demo::upCast(Calc* p) { return p; }

void
::IceProxy::Demo::_readProxy(::Ice::InputStream* istr, ::IceInternal::ProxyHandle< Calc>& v)
{
    ::Ice::ObjectPrx proxy;
    istr->read(proxy);
    if(!proxy)
    {
        v = 0;
    }
    else
    {
        v = new Calc;
        v->_copyFrom(proxy);
    }
}
/// \endcond

::Ice::AsyncResultPtr
IceProxy::Demo::Calc::_iceI_begin_add(::Ice::Int iceP_a, ::Ice::Int iceP_b, const ::Ice::Context& context, const ::IceInternal::CallbackBasePtr& del, const ::Ice::LocalObjectPtr& cookie, bool sync)
{
    _checkTwowayOnly(iceC_Demo_Calc_add_name, sync);
    ::IceInternal::OutgoingAsyncPtr result = new ::IceInternal::CallbackOutgoing(this, iceC_Demo_Calc_add_name, del, cookie, sync);
    try
    {
        result->prepare(iceC_Demo_Calc_add_name, ::Ice::Normal, context);
        ::Ice::OutputStream* ostr = result->startWriteParams(::Ice::DefaultFormat);
        ostr->write(iceP_a);
        ostr->write(iceP_b);
        result->endWriteParams();
        result->invoke(iceC_Demo_Calc_add_name);
    }
    catch(const ::Ice::Exception& ex)
    {
        result->abort(ex);
    }
    return result;
}

::Ice::Long
IceProxy::Demo::Calc::end_add(const ::Ice::AsyncResultPtr& result)
{
    ::Ice::AsyncResult::_check(result, this, iceC_Demo_Calc_add_name);
    ::Ice::Long ret;
    if(!result->_waitForResponse())
    {
        try
        {
            result->_throwUserException();
        }
        catch(const ::Ice::UserException& ex)
        {
            throw ::Ice::UnknownUserException(__FILE__, __LINE__, ex.ice_id());
        }
    }
    ::Ice::InputStream* istr = result->_startReadParams();
    istr->read(ret);
    result->_endReadParams();
    return ret;
}

::Ice::AsyncResultPtr
IceProxy::Demo::Calc::_iceI_begin_subtract(::Ice::Int iceP_a, ::Ice::Int iceP_b, const ::Ice::Context& context, const ::IceInternal::CallbackBasePtr& del, const ::Ice::LocalObjectPtr& cookie, bool sync)
{
    _checkTwowayOnly(iceC_Demo_Calc_subtract_name, sync);
    ::IceInternal::OutgoingAsyncPtr result = new ::IceInternal::CallbackOutgoing(this, iceC_Demo_Calc_subtract_name, del, cookie, sync);
    try
    {
        result->prepare(iceC_Demo_Calc_subtract_name, ::Ice::Normal, context);
        ::Ice::OutputStream* ostr = result->startWriteParams(::Ice::DefaultFormat);
        ostr->write(iceP_a);
        ostr->write(iceP_b);
        result->endWriteParams();
        result->invoke(iceC_Demo_Calc_subtract_name);
    }
    catch(const ::Ice::Exception& ex)
    {
        result->abort(ex);
    }
    return result;
}

::Ice::Long
IceProxy::Demo::Calc::end_subtract(const ::Ice::AsyncResultPtr& result)
{
    ::Ice::AsyncResult::_check(result, this, iceC_Demo_Calc_subtract_name);
    ::Ice::Long ret;
    if(!result->_waitForResponse())
    {
        try
        {
            result->_throwUserException();
        }
        catch(const ::Ice::UserException& ex)
        {
            throw ::Ice::UnknownUserException(__FILE__, __LINE__, ex.ice_id());
        }
    }
    ::Ice::InputStream* istr = result->_startReadParams();
    istr->read(ret);
    result->_endReadParams();
    return ret;
}

::Ice::AsyncResultPtr
IceProxy::Demo::Calc::_iceI_begin_op(const ::Demo::A& iceP_a1, ::Ice::Short iceP_b1, const ::Ice::Context& context, const ::IceInternal::CallbackBasePtr& del, const ::Ice::LocalObjectPtr& cookie, bool sync)
{
    ::IceInternal::OutgoingAsyncPtr result = new ::IceInternal::CallbackOutgoing(this, iceC_Demo_Calc_op_name, del, cookie, sync);
    try
    {
        result->prepare(iceC_Demo_Calc_op_name, ::Ice::Normal, context);
        ::Ice::OutputStream* ostr = result->startWriteParams(::Ice::DefaultFormat);
        ostr->write(iceP_a1);
        ostr->write(iceP_b1);
        result->endWriteParams();
        result->invoke(iceC_Demo_Calc_op_name);
    }
    catch(const ::Ice::Exception& ex)
    {
        result->abort(ex);
    }
    return result;
}

void
IceProxy::Demo::Calc::end_op(const ::Ice::AsyncResultPtr& result)
{
    _end(result, iceC_Demo_Calc_op_name);
}

/// \cond INTERNAL
::IceProxy::Ice::Object*
IceProxy::Demo::Calc::_newInstance() const
{
    return new Calc;
}
/// \endcond

const ::std::string&
IceProxy::Demo::Calc::ice_staticId()
{
    return ::Demo::Calc::ice_staticId();
}

Demo::Calc::~Calc()
{
}

/// \cond INTERNAL
::Ice::Object* Demo::upCast(Calc* p) { return p; }

/// \endcond

namespace
{
const ::std::string iceC_Demo_Calc_ids[2] =
{
    "::Demo::Calc",
    "::Ice::Object"
};

}

bool
Demo::Calc::ice_isA(const ::std::string& s, const ::Ice::Current&) const
{
    return ::std::binary_search(iceC_Demo_Calc_ids, iceC_Demo_Calc_ids + 2, s);
}

::std::vector< ::std::string>
Demo::Calc::ice_ids(const ::Ice::Current&) const
{
    return ::std::vector< ::std::string>(&iceC_Demo_Calc_ids[0], &iceC_Demo_Calc_ids[2]);
}

const ::std::string&
Demo::Calc::ice_id(const ::Ice::Current&) const
{
    return ice_staticId();
}

const ::std::string&
Demo::Calc::ice_staticId()
{
#ifdef ICE_HAS_THREAD_SAFE_LOCAL_STATIC
    static const ::std::string typeId = "::Demo::Calc";
    return typeId;
#else
    return iceC_Demo_Calc_ids[0];
#endif
}

/// \cond INTERNAL
bool
Demo::Calc::_iceD_add(::IceInternal::Incoming& inS, const ::Ice::Current& current)
{
    _iceCheckMode(::Ice::Normal, current.mode);
    ::Ice::InputStream* istr = inS.startReadParams();
    ::Ice::Int iceP_a;
    ::Ice::Int iceP_b;
    istr->read(iceP_a);
    istr->read(iceP_b);
    inS.endReadParams();
    ::Ice::Long ret = this->add(iceP_a, iceP_b, current);
    ::Ice::OutputStream* ostr = inS.startWriteParams();
    ostr->write(ret);
    inS.endWriteParams();
    return true;
}
/// \endcond

/// \cond INTERNAL
bool
Demo::Calc::_iceD_subtract(::IceInternal::Incoming& inS, const ::Ice::Current& current)
{
    _iceCheckMode(::Ice::Normal, current.mode);
    ::Ice::InputStream* istr = inS.startReadParams();
    ::Ice::Int iceP_a;
    ::Ice::Int iceP_b;
    istr->read(iceP_a);
    istr->read(iceP_b);
    inS.endReadParams();
    ::Ice::Long ret = this->subtract(iceP_a, iceP_b, current);
    ::Ice::OutputStream* ostr = inS.startWriteParams();
    ostr->write(ret);
    inS.endWriteParams();
    return true;
}
/// \endcond

/// \cond INTERNAL
bool
Demo::Calc::_iceD_op(::IceInternal::Incoming& inS, const ::Ice::Current& current)
{
    _iceCheckMode(::Ice::Normal, current.mode);
    ::Ice::InputStream* istr = inS.startReadParams();
    A iceP_a1;
    ::Ice::Short iceP_b1;
    istr->read(iceP_a1);
    istr->read(iceP_b1);
    inS.endReadParams();
    this->op(iceP_a1, iceP_b1, current);
    inS.writeEmptyParams();
    return true;
}
/// \endcond

namespace
{
const ::std::string iceC_Demo_Calc_all[] =
{
    "add",
    "ice_id",
    "ice_ids",
    "ice_isA",
    "ice_ping",
    "op",
    "subtract"
};

}

/// \cond INTERNAL
bool
Demo::Calc::_iceDispatch(::IceInternal::Incoming& in, const ::Ice::Current& current)
{
    ::std::pair<const ::std::string*, const ::std::string*> r = ::std::equal_range(iceC_Demo_Calc_all, iceC_Demo_Calc_all + 7, current.operation);
    if(r.first == r.second)
    {
        throw ::Ice::OperationNotExistException(__FILE__, __LINE__, current.id, current.facet, current.operation);
    }

    switch(r.first - iceC_Demo_Calc_all)
    {
        case 0:
        {
            return _iceD_add(in, current);
        }
        case 1:
        {
            return _iceD_ice_id(in, current);
        }
        case 2:
        {
            return _iceD_ice_ids(in, current);
        }
        case 3:
        {
            return _iceD_ice_isA(in, current);
        }
        case 4:
        {
            return _iceD_ice_ping(in, current);
        }
        case 5:
        {
            return _iceD_op(in, current);
        }
        case 6:
        {
            return _iceD_subtract(in, current);
        }
        default:
        {
            assert(false);
            throw ::Ice::OperationNotExistException(__FILE__, __LINE__, current.id, current.facet, current.operation);
        }
    }
}
/// \endcond

/// \cond STREAM
void
Demo::Calc::_iceWriteImpl(::Ice::OutputStream* ostr) const
{
    ostr->startSlice(ice_staticId(), -1, true);
    ::Ice::StreamWriter< Calc, ::Ice::OutputStream>::write(ostr, *this);
    ostr->endSlice();
}

void
Demo::Calc::_iceReadImpl(::Ice::InputStream* istr)
{
    istr->startSlice();
    ::Ice::StreamReader< Calc, ::Ice::InputStream>::read(istr, *this);
    istr->endSlice();
}
/// \endcond

/// \cond INTERNAL
void
Demo::_icePatchObjectPtr(CalcPtr& handle, const ::Ice::ObjectPtr& v)
{
    handle = CalcPtr::dynamicCast(v);
    if(v && !handle)
    {
        IceInternal::Ex::throwUOE(Calc::ice_staticId(), v);
    }
}
/// \endcond

namespace Ice
{
}

#endif
